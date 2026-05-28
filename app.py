import simpy
import mapa_grafos as mg

class DeliveryMoto:
    def __init__(self, env, id_moto, mapa, origen, destino):
        self.env = env
        self.id_moto = id_moto
        self.mapa = mapa
        self.origen = origen
        self.destino = destino
        self.velocidad = 40 # km/h

        #inicio mi clase automaticamente cuando llamo a la clase para la simulacion
        self.proceso = env.process(self.run())

    def run(self):
            """Bucle principal del comportamiento del camión (Proceso SimPy)"""
            print(f"[{self.env.now:.2f} min] 🚛 Camión {self.id} encendido en {self.nodo_actual}.")
            
            # Calcular ruta inicial
            ruta = self.mapa.calcular_ruta(self.nodo_actual, self.destino_final)
            
            while self.nodo_actual != self.destino_final:
                siguiente_nodo = ruta[ruta.index(self.nodo_actual) + 1]
                
                # Verificar si el tramo que viene está libre
                if self.mapa.G[self.nodo_actual][siguiente_nodo]['bloqueada']:
                    print(f"[{self.env.now:.2f} min] ⚠️ Camión {self.id} ve tramo trancado. Recalculando...")
                    ruta = self.mapa.calcular_ruta(self.nodo_actual, self.destino_final)
                    if not ruta:
                        print(f"[{self.env.now:.2f} min] ❌ Camión {self.id} varado. No hay desvíos disponibles.")
                        return
                    siguiente_nodo = ruta[1] # Tomar el primer paso de la nueva ruta
                
                # Viajar
                distancia = self.mapa.G[self.nodo_actual][siguiente_nodo]['distancia']
                tiempo_viaje = (distancia / self.velocidad) * 60
                
                yield self.env.timeout(tiempo_viaje)
                self.nodo_actual = siguiente_nodo
                print(f"[{self.env.now:.2f} min] 📍 Camión {self.id} llegó a {self.nodo_actual}")
                
            print(f"[{self.env.now:.2f} min] 🎉 Camión {self.id} completó entrega en {self.destino_final}.")


# Entorno de ejecución
if __name__ == "__main__":
    env = simpy.Environment()
    mapa = mg.MapaParaguana()
    
    # Instanciamos camiones como objetos autónomos
    camion1 = DeliveryMoto(env, "FarmaNorte-01", mapa, "Las_Margaritas", "Hospital_Calle_Sierra")

    ruta = mg.MapaParaguana.calcular_dijkstra(camion1)
    
    # Podemos meter un evento rápido usando una función generadora simple de SimPy
    evento_accidente = mg.MapaParaguana.obstruir_paso("Las_Margaritas", "Hospital_Calle_Sierra")
        
    env.process(evento_accidente)
    env.run(until=30)