#ahora ya no es solo nodo por que aqui vamos a trabajar sobre el mapa
extends Node2D

#creamos una ruta para el nodo de la moto para llamarlo
@onready var nodo_moto = $ContenedorMoto/Moto
#hacemos otro onready para llamar a la interfaz para enviar le destino a python
@onready var interfaz_destino: InterfazLogitica = $Interfaz_Usuario

#aqui es donde vamos a dejar la ruta completa cuando se python nos las pase
var ruta_completa_dijktra: Array = []

#igual que antes creamos una funcion principal de godot que va escuchar lo que tengo que decir otros mudulos 
func _ready() -> void:
	#aqui lo que hacemos es escuchar si el modulo de conexion envio datos 
	ConexionPython.ruta_python.connect(_visualizacion_rutas)
	#hacemos la conexion con la interfaz
	interfaz_destino.destino_seleccionado.connect(_on_destino_recibido)

#aqui es donde vamos a manejar los evento que puedan sucerder
func _visualizacion_rutas(evento: String, datos: Dictionary) -> void:
	match evento:
		"Moto_Ruta":
			var ruta_lista = datos.get("Ruta")
			
		"Moto_en_Camino":
			var camino = datos.get("Datos")
			if camino != null:
				_moto_en_camnino(camino)
			else:
				print("ajajajajjajaajajajajajaj la interfaz funciona NOJODA")

#aqui enviamos a python el destino final para iniciar el calculo de la ruta
func _on_destino_recibido(destino_escogido: String) -> void:
	#enviamos la destino al comando que encedera toda la logica de python
	ConexionPython.enviar_arranque_moto(destino_escogido)

#aqui hacemos la logica para no salurar nuestra funcion principal
func _moto_en_camnino(datos_a_usar: Dictionary) -> void:
	var origen = datos_a_usar.get("Origen")
	var destino = datos_a_usar.get("Destino")
	
	
	
	
	
	
