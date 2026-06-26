#ahora ya no es solo nodo por que aqui vamos a trabajar sobre el mapa
extends Control

#creamos una ruta para el nodo de la moto para llamarlo
@onready var nodo_moto = $Entidades_Simulacion/Moto
@onready var lineas_rutas = $Entidades_Simulacion/Rutas_Lineas
const GestorVisual = preload("res://gestor_visual.gd")
var gestor_visual = GestorVisual.new()

#creamos una señal para enviarle los datos a los dashboard
signal datos_viaje(datos: Dictionary)

#estas son todas nuestras variables globales
#aqui es donde vamos a dejar la ruta completa cuando se python nos las pase
var ruta_completa_dijkstra: Array = []
#aqui guardamos las coordenadas (x,y)
var coordenadas: Array[Vector2] = []
var mapa_indices: Dictionary = {}
#el indice para la interacion entre nodos 
var indice_actual: int = 0
#veficamos si estamos viajando
var viajando: bool = false
#aqui es donde estara la distancia 
var distancia: int = 0
#y aqui es donde colocaremos el tiempo
var tiempo: int = 0
var actualizar_nodo: String = ""
var estado: String = ""

#igual que antes creamos una funcion principal de godot que va escuchar lo que tengo que decir otros mudulos 
func _ready() -> void:
	print("naci")
	
	await get_tree().process_frame
	
	var interfaz_destino = $Interfaz_Usuario/Node2D
	
	interfaz_destino.destino_seleccionado.connect(_on_destino_recibido)
	print("conectado a la interfaz")
	
	#le decimos donde enviar los datos de la interfaz a la funcion dentro de la interfaz para actualzar los datos
	datos_viaje.connect(interfaz_destino._on_actualizar_interfaz)
	
	nodo_moto.enviar_nodo.connect(_on_moto_llego_a_nodo)
	nodo_moto.velocidad_actualizada.connect(_on_moto_velocidad_cambio)
	
	#aqui lo que hacemos es escuchar si el modulo de conexion envio datos 
	ConexionPython.ruta_python.connect(_controlador)
	
#aqui es donde vamos a manejar los evento que puedan sucerder
func _controlador(evento: String, datos: Dictionary) -> void:
	if evento == "Moto_en_Camino":
		print("python envio los datos de la moto 🤑")
		var dic = datos.get("Datos", [])
		estado = dic["Estado"]
		distancia = dic["Distancia"]
		tiempo = dic["Tiempo"]
		viajando = true
		
		ruta_completa_dijkstra = dic["Ruta"]
		var lugar = get_node("Entidades_Simulacion")
		#llamamos a nuestra funcion para convertilo en coordenadas
		var resultado = gestor_visual._convertir_ruta(lugar, ruta_completa_dijkstra)
		
		coordenadas = resultado["coordenadas"]
		mapa_indices = resultado["mapa"]
		var nombre_objetivo = mapa_indices.get(0, "punto_inicial")
		
		gestor_visual.visualizar_ruta(ruta_completa_dijkstra, lineas_rutas)
		
		indice_actual = 0
		nodo_moto.coordenadas = coordenadas
		nodo_moto.establecer_objetivo(coordenadas[indice_actual], nombre_objetivo)
		
		print("gracias python ahora puedo calcular")
		
		var mensaje_interfaz = {
			"Tipo": "Datos_Generales",
			"Estado": estado,
			"Distancia": distancia,
			"Tiempo": tiempo,
			"Ruta_Completa_Dijkstra": ruta_completa_dijkstra
		}
		
		datos_viaje.emit(mensaje_interfaz)
		
	elif evento == "No_Obstruccion":
		print("camino despejado")
		viajando = true
		actualizar_nodo = datos.get("Nodo")
		
		
		if indice_actual < coordenadas.size():
			# Pasamos el nombre si es un nodo de Python, o "" si es cruce
			# Aquí podrías agregar lógica para saber qué nombre pasar
			nodo_moto.establecer_objetivo(coordenadas[indice_actual], "")
		
		var actualizacion = {
			"Tipo": "Nodo1",
			"Siguiente_Nodo": actualizar_nodo
		}
		
		datos_viaje.emit(actualizacion)
	
	elif evento == "Es_Cruce":
		print("mano estamos crusando aviso cualquier cosa")
		nodo_moto.establecer_objetivo(coordenadas[indice_actual], "")
		
	elif evento == "Entrega_Completada":
		estado = datos.get("Estado")
		var otro_mensaje = {
			"Estado": estado
		}
		datos_viaje.emit(otro_mensaje)
		
		viajando = false
		
#aqui enviamos a python el destino final para iniciar el calculo de la ruta
func _on_destino_recibido(destino_escogido: String) -> void:
	#hacemos una pequeña verificacion antes de enviar el comando
	if not ConexionPython.conectado:
		print("mano espara un momento que bugea todo")
		return
	
	print("los datos de la interfaz llegaron")
	#enviamos la destino al comando que encedera toda la logica de python
	ConexionPython.enviar_arranque_moto(destino_escogido)

func _on_moto_llego_a_nodo(_nombre_nodo: String) -> void:
	print("wuajuuuuu")
	indice_actual += 1
	
	var progreso = float(indice_actual) / float(coordenadas.size())
	datos_viaje.emit({"Tipo": "Progreso", "Valor": progreso})
	
	if indice_actual < coordenadas.size():
		print("wario por que wario nose")
		var tipo = mapa_indices.get(indice_actual, "Cruce")
		
		ConexionPython.enviar_json({
			"Comando": "Llegue_Nodo",
			"Indice": indice_actual,
			"Tipo": tipo
		})

func _on_moto_velocidad_cambio(nueva_velocidad: float):
	var paquete = {
		"Tipo": "Velocidad",
		"Valor": nueva_velocidad
	}
	datos_viaje.emit(paquete)
