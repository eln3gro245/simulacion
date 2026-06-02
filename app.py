import websockets
import asyncio
import simpy
import json
import mapa_grafos as mg

class DeliveryMoto:
    def __init__(self, env, id_moto, mapa):
        self.env = env
        self.id_moto = id_moto
        self.mapa = mapa
        self.nodo_actual = "centro"
        self.velocidad = 40 # km/h

        #aqui asignamos una atributo para mandar la ruta calcula mendiate dijkstra para que se muestre en el godot
        self.ruta_dijkstra = []

        #inicio mi clase automaticamente cuando llamo a la clase para la simulacion
        self.proceso = env.process(self.run())
        #creamos una lista que almanace la ruta ya definida
        self.historial = [self.nodo_actual]

    def run(self, destino):
        #aqui es donde vamos a correr la simulación
        print(f"Tiempo Transcurrido: {self.env.now:.2f} Minutos \n La Moto {self.id_moto} en Direccion desde {self.nodo_actual.title()} hasta {destino.title()}")

        #hacemos el calculo de la ruta mediante dijkstra
        self.ruta_dijkstra = self.mapa.calcular_dijkstra(self.nodo_actual, destino)

        #esta es la logica para que define el movimiento de la moto entre los nodos 
        while self.nodo_actual != destino:
            siguiente_nodo = self.ruta_dijkstra[self.ruta_dijkstra.index(self.nodo_actual) + 1]

            #en esta parte verificamos si el camino(o ruta) esta despejada
            if self.mapa.G[self.nodo_actual][siguiente_nodo]['bloqueada']:
                print(f"Tiempo Transcurrido: {self.env.now:.2f} Minutos \n La Moto {self.id_moto} se encontro una calle bloqueada \n recalculando...")
                #se llama ruta alternativa para que podemas determinar los posibles camino si esta atascado
                ruta_alternativa = self.mapa.calcular_dijkstra(self.nodo_actual, destino)

                if not ruta_alternativa:
                    #vemos nuestro historial para lograr devolvernos si no hay camino
                    if len(self.historial) > 1:
                        #ahora medieante le historial nos devolvemos
                        nodo_anterior = self.historial[-2]

                        print(f"Tiempo Transcurrido: {self.env.now:.2f} Minutos \n La Moto {self.id_moto} volviendo a {nodo_anterior} para recalcular \n volviendo...")

                        #forzamos el cambio de nodo
                        self.ruta_dijkstra = self.mapa.calcular_dijkstra(self.nodo_actual, nodo_anterior)
                
                else:
                    self.ruta_dijkstra = ruta_alternativa
                    siguiente_nodo = self.ruta_dijkstra[1]
        
            #aqui estan los datos que genero la simulacion
            distancia = self.mapa.G[self.nodo_actual][siguiente_nodo]['distancia']
            tiempo_del_viaje = (distancia / self.velocidad) * 60

            yield self.env.timeout(tiempo_del_viaje)

    async def enviar_ruta(self, websocket, pedido=False):
        #aqui mandamos la ruta ya calculada por dikjstra para que se puede visualzar en el godot
        if pedido == True:
            mensaje_ruta = {
            "Evento": "Moto_ruta",
            "Ruta": self.ruta_dijkstra
            }

            await websocket.send(json.dumps(mensaje_ruta))
        else:
            #damos un mensaje de alerta para ser visualizado en godot 
            mensaje_alerta = {"Alerta": "Error", "Mensaje": "Inserte una Ruta para Visualizar la Ruta"}
            await websocket.send(json.dumps(mensaje_alerta))
            
        
            

#esta funcion es la que se encagara de la conexion entre el python y el godot
async def manejo_server_godot(websocket, mapa):
    try:
        #aqui esperamos la primera peticion para activar la simulacion
        async for mensaje in websocket:
            peticion = json.loads(mensaje)

            env_simpy = simpy.Environment()

            #aqui confirmamos el encabezado del json que determina que accion hace la moto
            if peticion.get("Comando") == "Arrancar_Moto":
                moto = peticion["Moto"]
                id_moto = moto["Id_Moto"]
                destino = moto["Destino"]

                moto = DeliveryMoto(env_simpy, id_moto, mapa)

                #luego aqui con los datos moto proporcionados por el godot ejecutamos la logica del grafo
                moto.run(destino)

                #ahora dentro de python realizamos nosotros la peticion desde python
                mensaje_json = {
                    "Evento": "Moto_en_Camino",
                    "Datos": {
                        "Estado": "Procesando_Ruta",
                        "Origen": moto.nodo_actual,
                        "Destino": destino
                    }
                }

                await websocket.send(json.dumps(mensaje_json))

                pedido = True

                #aqui enviamos la ruta calcula por dijkstra
                await moto.enviar_ruta(websocket, pedido)

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

async def conexion_server():
    #aqui vamos a hacer uso de todas la funciones para y mantener la conexion con el godot
    mapa = mg.MapaParaguana() #este es el mapa que esta hecho con grafos para dar sentido a las cosas dentro del godot

    #activo el servidor y lo dejo escuchando peticiones del godot
    async with websockets.serve(
        lambda ws: manejo_server_godot(ws, mapa),
        "localhost",
        8765
    ):
    
        await asyncio.Future() #esto mantiene activo el puerto para recibir y enviar peticiones


# Entorno de ejecución
if __name__ == "__main__":
    asyncio.run(conexion_server())
    