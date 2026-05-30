from ursina import *
import mapa_grafos as M

app = Ursina()
mapa = M.MapaParaguana()
moto = M.DeliveryMoto()

if __name__ == "__main__":

    mapa.construir_Punto_Fijo()
    mapa.constriuir_Distribuidor_El_Sabino()

    app.run()