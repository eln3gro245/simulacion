import simpy
import mapa_grafos as mg

class DeliveryMoto:
    def __init__(self, env, id_moto, mapa, origen):
        self.env = env
        self.id_moto = id_moto
        self.mapa = mapa
        self.nodo_actual = origen
        self.velocidad = 40 # km/h

        #inicio mi clase automaticamente cuando llamo a la clase para la simulacion
        self.proceso = env.process(self.run())
        #creamos una lista que almanace la ruta ya definida
        self.historial = [origen]

    def run(self, destino):
        #aqui es donde vamos a correr la simulación
        print(f"Tiempo Transcurrido: {self.env.now:.2f} Minutos \n La Moto {self.id_moto} en Direccion desde {self.nodo_actual.title()} hasta {destino.title()}")

        #hacemos el calculo de la ruta mediante dijkstra
        ruta = self.mapa.calcular_dijkstra(self.nodo_actual, destino)

        #esta es la logica para que define el movimiento de la moto entre los nodos 
        while self.nodo_actual != destino:
            siguiente_nodo = ruta[ruta.index(self.nodo_actual) + 1]

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
                        ruta = self.mapa.calcular_dijkstra(self.nodo_actual, nodo_anterior)
                
                else:
                    ruta = ruta_alternativa
                    siguiente_nodo = ruta[1]
        
            #aqui estan los datos que genero la simulacion
            distancia = self.mapa.G[self.nodo_actual][siguiente_nodo]['distancia']
            tiempo_del_viaje = (distancia / self.velocidad) * 60

            yield self.env.timeout(tiempo_del_viaje)


                    

# Entorno de ejecución
if __name__ == "__main__":
    pass