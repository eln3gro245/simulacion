import networkx as nx
#extraemos las librerias que usaremos para la simulacion y el calculo de las distancias

class MapaParaguana:
    def __init__(self):
        self.G = nx.Graph()
        #con este metodo creamos la funcion para crear los nodos de punto fijo
        self.construir_Punto_Fijo()
        self.constriuir_Distribuidor_El_Sabino()

    def construir_Punto_Fijo(self):
        #aqui vamos a construir punto fijo de manera que todo sea mas simple de ver, a manera de nodo
        #estos son los nodos que representa a punto fijo
        self.G.add_node("Centro", pos=(2, 8))
        self.G.add_node("Las_Margaritas", pos=(4, 9))
        self.G.add_node("Maraven", pos=(3, 3))
        self.G.add_node("La_Puerta", pos=(5, 1))
        self.G.add_node("Punta_Cardon", pos=(1, 1))

        #estas son las conexiones entre cada nodo (aristas) la distacia esta en kilometros
        self.G.add_edge("Centro", "Las_Margaritas", distancia=5.0, bloqueada=False)
        self.G.add_edge("Centro", "Maraven", distancia=6.5, bloqueada=False)
        self.G.add_edge("Centro", "Punta_Cardon", distancia=8.0, bloqueada=False)
        self.G.add_edge("Maraven", "La_Puerta", distancia=3.5, bloqueada=False)
        self.G.add_edge("Maraven", "Punta_Cardon", distancia=4.0, bloqueada=False)
        self.G.add_edge("Las_Margaritas", "La_Puerta", distancia=5.0, bloqueada=False)

    def constriuir_Distribuidor_El_Sabino(self):
        #hacemos el mismo procedimiento antes para el Sabino
        self.G.add_node("Distribuidor_El_Sabino", pos=(6, 8))
        self.G.add_node("UNEFA", pos=(7, 7))
        self.G.add_node("Zona_Franca", pos=(8, 6))
        self.G.add_node("Comunidad_Cardon", pos=(5, 5))
        self.G.add_node("Hospital_Calle_Sierra", pos=(2, 10))

        #igual antes estas son las conexiones (airstas) para el Sabino
        self.G.add_edge("Distribuidor_El_Sabino", "UNEFA", distancia=1.5, bloqueada=False)
        self.G.add_edge("Distribuidor_El_Sabino", "Zona_Franca", distancia=3.0, bloqueada=False)
        self.G.add_edge("Distribuidor_El_Sabino", "Comunidad_Cardon", distancia=4.5, bloqueada=False)
        self.G.add_edge("Distribuidor_El_Sabino", "Hospital_Calle_Sierra", distancia=5.5, bloqueada=False)
        #ruta alterna
        self.G.add_edge("Zona_Franca", "Comunidad_Cardon", distancia=3.5, bloqueada=False)

        #para la entrada y salida entre el Sabino y Punto Fijo
        self.G.add_edge("Distribuidor_El_Sabino", "Las_Margaritas", distancia=2.0, bloqueada=False)

    def calcular_dijkstra(self, origen, destino):
        #aqui es donde calculamos la ruta mas optima entre los distintos nodos tambien toma en encuenta si la arista esta ocupada
        try:
            return nx.shortest_path(
                self.G,
                source=origen,
                target=destino,
                weight=lambda u, v, d: float('inf') if d['bloqueada'] else d['distancia']
            )
        except nx.NetworkXNoPath:
            return None
        
    def obstruir_paso(self, origen, destino, bloqueada=True):
        if self.G.has_edge(origen, destino):
            self.G[origen][destino]["bloqueada"] = "bloqueada"

