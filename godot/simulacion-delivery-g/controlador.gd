#ahora ya no es solo nodo por que aqui vamos a trabajar sobre el mapa
extends Node2D

#igual que antes creamos una funcion principal de godot que va escuchar lo que tengo que decir otros mudulos 
func _ready() -> void:
	#aqui lo que hacemos es escuchar si el modulo de conexion envio datos 
	ConexionPython.ruta_python.connect(_visualizacion_rutas)

#aqui es donde vamos a manejar los evento que puedan sucerder
func _visualizacion_rutas(evento: String, datos: Dictionary) -> void:
	match evento:
		"Moto_Ruta":
			var ruta_lista = datos.get("Ruta")
			
		"Moto_en_Camino":
			pass
