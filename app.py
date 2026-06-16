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
        #verificamos donde estamos ahora
        try:
            indice = self.ruta_dijkstra.index(nodo_alcanzado)
        except ValueError:
            print("denrto de la ruta no existe ese nodo")
        
        #verificamos si llegamos al nodo final
        if indice == len(self.ruta_dijkstra) - 1:
            await websocket.send(json.dumps({"Evento": "Entrega_Completada"}))
            return

        #ahora que verificamos todo podemos movernos
        print("nos movemos 😎")
        siguiente_nodo = self.ruta_dijkstra[indice + 1]

        #ahora cerificamos si hay un bloqueo
        if self.mapa.G[nodo_alcanzado][siguiente_nodo]["bloqueada"]:
            #le decimos a dijkstra que estamos en el ultimo nodo alcanzado
            self.nodo_actual = nodo_alcanzado
            self.ruta_dijkstra = self.mapa.calcular_dijkstra(self.nodo_actual, self.destino)

            mensaje_json = {
                "Evento": "Moto_en_Camino",
                "Datos": {
                    "Estado": "Procesando_Ruta",
                    "Origen": self.nodo_actual,
                    "Destino": self.destino,
                    "Ruta": self.ruta_dijkstra
                }
            }
            #se lo enviamos con la nueva ruta
            await websocket.send(json.dumps(mensaje_json))
        else:
            await websocket.send(json.dumps({"Evento": "No_Obstruccion"}))
            print("pase rey")
                
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

                print(f"mi amorsito me escribio a ver que dice. Moto ID: {id_moto} | Destino: {destino}")
                

                moto = DeliveryMoto(env_simpy, id_moto, mapa, destino)

                #luego aqui con los datos moto proporcionados por el godot ejecutamos la logica del grafo
                moto.ruta_optima()

                print(f"Dijkstra chambea: {moto.ruta_dijkstra}")

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

                await websocket.send(json.dumps(mensaje_json))
                print("carta de amor de python para godot no espiar")

            elif peticion.get("Comando") == "Llegue_Nodo":
                print("yaju nos movimos seria justicia")
                nodo_alcanzado = peticion["Nodo"]
                print(f"este es el nodo a donde vamos: {nodo_alcanzado}")

                
                await moto.nodo_parada(websocket, nodo_alcanzado)
                    

            elif peticion.get("Comando") == "Obtruir_Paso":
                print("QUE POR AQUI NO ALV")
                ruta = peticion["Ruta"]
                origen2 = ruta["origen"]
                destino2 = ruta["destino"]

                mapa.obstruir_paso(origen2, destino2)
                print("no pasaras🤑")

                obstruccion_json = {
                    "Evento": "Obstrucion_Camino",
                    "Datos": {
                        "Estado": "bloqueada",
                        "Origen": origen2,
                        "Destino": destino2
                    }
                }

                await websocket.send(json.dumps(obstruccion_json))
                print("godot que paso rey ya respondeme 😭")

    except websockets.exceptions.ConnectionClosedOK:
        print("conexion terminada")

    except websockets.exceptions.ConnectionClosedError:
        print("godot yo te amo no me abandones")
        
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

    #inicializo las funciones del grafo del el sabino y punto fijo
    mapa.construir_Punto_Fijo() #creamos punto fijo
    mapa.constriuir_Distribuidor_El_Sabino() #creamos el sabino

    print("Mapa construido con nodos:", list(mapa.G.nodes()))

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
    