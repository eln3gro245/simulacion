from functools import partial
import mapa_grafos as mg
import websockets
import asyncio
import simpy
import json

class DeliveryMoto:
    def __init__(self, env, id_moto, mapa, destino):
        self.env = env
        self.id_moto = id_moto
        self.mapa = mapa
        self.nodo_actual = "Centro"
        self.velocidad = 40 # km/h
        self.destino = destino

        #aqui asignamos una atributo para mandar la ruta calcula mendiate dijkstra para que se muestre en el godot
        self.ruta_dijkstra = []
        #ahora guardamos las rutas para hacer calculos de acuerdo a las obstruciones
        self.historial = [self.nodo_actual]


    def ruta_optima(self):
        #hacemos el calculo de la ruta mediante dijkstra
        self.ruta_dijkstra = self.mapa.calcular_dijkstra(self.nodo_actual, self.destino)

    async def nodo_parada(self, websocket, nodo_alcanzado):
        #aqui es donde estamos ahora
        self.historial.append(self.nodo_actual)
        #y aqui es a donde iremos despues
        self.nodo_actual = nodo_alcanzado

        if self.nodo_actual == self.destino:
            print("destino alcazado")
            await websocket.send(json.dumps({"Evento": "Entrega_Completada"}))
            return
        
        indice_actual = self.ruta_dijkstra.index(self.nodo_actual)
        siguiente_nodo = self.ruta_dijkstra[indice_actual + 1]

        if self.mapa.G[self.nodo_actual][siguiente_nodo]['bloqueada']:
            print("recalculando")

            self.ruta_dijkstra = self.mapa.calcular_dijkstra(self.nodo_actual, self.destino)

            await self.enviar_ruta(websocket, pedido=True)
            print("nueva ruta asignada")
        
        else:
            await websocket.send(json.dumps({"Evento": "Moto_en_Camido"}))
            
#esta funcion es la que se encagara de la conexion entre el python y el godot
async def manejo_server_godot(websocket, mapa):
    print("nos llamo la funcion anterior")
    moto = None
    try:
        #aqui esperamos la primera peticion para activar la simulacion
        async for mensaje in websocket:
            print("llego un mensaje", flush=True)
            peticion = json.loads(mensaje)

            env_simpy = simpy.Environment()

            #aqui confirmamos el encabezado del json que determina que accion hace la moto
            if peticion.get("Comando") == "Arrancar_Moto":
                moto = peticion["Moto"]
                id_moto = moto["Id_Moto"]
                destino = moto["Destino"]

                print(f"📥 [PYTHON] Comando Recibido. Moto ID: {id_moto} | Destino: {destino}")
                

                moto = DeliveryMoto(env_simpy, id_moto, mapa, destino)

                #luego aqui con los datos moto proporcionados por el godot ejecutamos la logica del grafo
                moto.ruta_optima()

                print(f"🗺️ [PYTHON] Ruta calculada por Dijkstra: {moto.ruta_dijkstra}")

                #ahora dentro de python realizamos nosotros la peticion desde python
                mensaje_json = {
                    "Evento": "Moto_en_Camino",
                    "Datos": {
                        "Estado": "Procesando_Ruta",
                        "Origen": moto.nodo_actual,
                        "Destino": destino,
                        "Ruta": moto.ruta_dijkstra
                    }
                }

            elif peticion.get("Comando") == "Llegue_Nodo":
                nodo_alcanzado = peticion["Nodo"]

                #verificamos si la moto existe
                if moto is not None:
                    await moto.nodo_parada(websocket, nodo_alcanzado)
                else:
                    print("falta la moto")

            elif peticion.get("Comando") == "Obtruir_Paso":
                ruta = peticion["Ruta"]
                origen2 = ruta["origen"]
                destino2 = ruta["destino"]

                obstruccion = mapa.obstruir_paso(origen2, destino2)

                obstruccion_json = {
                    "Evento": "Obstrucion_Camino",
                    "Datos": {
                        "Estado": "bloqueada",
                        "Origen": origen2,
                        "Destino": destino2
                    }
                }

                await websocket.send(json.dumps(obstruccion_json))

    except websockets.exceptions.ConnectionClosedOK:
        print("conexion terminada")

    except websockets.exceptions.ConnectionClosedError:
        print("la conexion fue cerrada de golpe")
        
    except json.JSONDecodeError:
        print("❌ [PYTHON ERROR] ¡Llegó un paquete corrupto o no es un JSON válido!")
        
    except Exception as e:
        print(f"💥 [PYTHON ERROR] Ocurrió un error inesperado en el bucle: {e}")
        
    finally:
        print("🧹 [PYTHON] Limpiando recursos de la conexión. Servidor listo para el siguiente intento.")

async def conexion_server():
    print("levantando servidor")
    #aqui vamos a hacer uso de todas la funciones para y mantener la conexion con el godot
    mapa = mg.MapaParaguana() #este es el mapa que esta hecho con grafos para dar sentido a las cosas dentro del godot

    #creamos una funcion clon para menejar de manera asicrona la conexion con godot
    funcion_clon = partial(manejo_server_godot, mapa=mapa)

    print("clon creado esperando el wedsocket")

    #activo el servidor y lo dejo escuchando peticiones del godot
    async with websockets.serve(
        funcion_clon,
        "127.0.0.1",
        8765
    ):
    
        await asyncio.Future() #esto mantiene activo el puerto para recibir y enviar peticiones
    
    print("serividor activo")


# Entorno de ejecución
if __name__ == "__main__":
    asyncio.run(conexion_server())
    