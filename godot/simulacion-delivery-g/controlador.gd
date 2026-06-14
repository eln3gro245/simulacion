#ahora ya no es solo nodo por que aqui vamos a trabajar sobre el mapa
extends Node2D

#creamos una ruta para el nodo de la moto para llamarlo
@onready var nodo_moto = $ContenedorMoto/Moto
#hacemos otro onready para llamar a la interfaz para enviar le destino a python
@onready var interfaz_destino: InterfazLogitica = $Interfaz_Usuario

#aqui es donde vamos a dejar la ruta completa cuando se python nos las pase
var ruta_completa_dijkstra: Array = []
#aqui guardamos las coordenadas (x,y)
var coordenadas: Array[Vector2] = []
#el indice para la interacion entre nodos 
var indice_actual: int = 0
#veficamos si estamos viajando
var viajando: bool = false
#velocidad de la moto(en pixeles)
var velocidad: float = 250.0

#igual que antes creamos una funcion principal de godot que va escuchar lo que tengo que decir otros mudulos 
func _ready() -> void:
	#aqui lo que hacemos es escuchar si el modulo de conexion envio datos 
	ConexionPython.ruta_python.connect(_controlador)
	#hacemos la conexion con la interfaz
	interfaz_destino.destino_seleccionado.connect(_on_destino_recibido)

#aqui es donde se ejecutaria el movimiento de la moto
func _process(delta: float) -> void:
	if not viajando or coordenadas.size() > 0:
		return
	
	#verificamos donde estamos dentro de la esena
	var destino_actual = coordenadas[indice_actual]
	$Moto.position = $Moto.position.move_toward(destino_actual, velocidad * delta)
	
	#ahora medimos las distancias para verificar si estamos en un nodo
	#tomamos un valor de tolerancia que nunca le valor va a hacer exacto (3 pixeles)
	if $Moto.position.distance_to(destino_actual) < 3.0:
		#ahora seguimos con el siguiente indice para continuar la ruta
		indice_actual += 1
		
		#ahora si ya es la ultima parada terminamos
		if indice_actual >= coordenadas.size():
			viajando = false
	

#aqui es donde vamos a manejar los evento que puedan sucerder
func _controlador(evento: String, datos: Dictionary) -> void:
	match evento:
		"Moto_Ruta":
			var ruta_completa_dijkstra = datos.get("Ruta", [])
			
			#llamamos a nuestra funcion para convertilo en coordenadas
			_convertir_ruta()
		"Moto_en_Camino":
			pass

#aqui enviamos a python el destino final para iniciar el calculo de la ruta
func _on_destino_recibido(destino_escogido: String = "Maraven") -> void:
	#enviamos la destino al comando que encedera toda la logica de python
	ConexionPython.enviar_arranque_moto(destino_escogido)

#aqui hacemos la logica para no saturar nuestra funcion principal
#vamos a traducir las pocisiones (x,y) de  godot para el desplazamiento de la moto
func _convertir_ruta() -> void:
	#borramos por si habia una coordenada anterior
	coordenadas.clear()
	indice_actual = 0
	
	for nombre_sector in ruta_completa_dijkstra:
		#buscamos le nodos actual en nuestra esena de godot
		var nodo_actual = get_node_or_null(nombre_sector)
		
		if nombre_sector:
			#ahora lo guardamos dentro de nuestras coordenadas
			coordenadas.append(nodo_actual.position)
			
	#una tengamos todo podemos iniciar le movimiento
	if coordenadas.size() > 0:
		viajando = true
	else:
		print("no se encontro una ruta valida verifique que se ha seleccionado un destino")
		
	
	
	
	
	
	
	
	
	
	
	
