extends Node2D


signal velocidad_actualizada(valor: float)
signal enviar_nodo(nombre: String)

#aqui guardamos las coordenadas (x,y)
var coordenadas: Array[Vector2] = []
#el indice para la interacion entre nodos 
var indice_actual: int = 0
#veficamos si estamos viajando
var viajando: bool = false
#velocidad de la moto(en pixeles)
var velocidad_inicial: float = 0.0
var velocidad_final: float = 200.0
#definimos una aceleracion para darle una apariencia de velocidad constante
var aceleracion: float = 50.0


var nodo_actual_nombre: String = "" # Aquí guardaremos el nombre del nodo objetivo
var destino_actual: Vector2 = Vector2.ZERO


func _physics_process(delta: float) -> void:
	if not viajando:
		return
	
	#verificamos donde estamos dentro de la esena
	var distancia_destino = position.distance_to(destino_actual)
	
	var velocidad_objetivo = velocidad_final
	if distancia_destino < 50.0:
		velocidad_objetivo = 200.0
	
	velocidad_inicial = move_toward(velocidad_inicial, velocidad_objetivo, aceleracion * delta)
	
	velocidad_actualizada.emit(snapped(velocidad_inicial, 0.01))
	
	position = position.move_toward(destino_actual, velocidad_inicial * delta)
	
	#ahora medimos las distancias para verificar si estamos en un nodo
	#tomamos un valor de tolerancia el valor nunca va a hacer exacto (3 pixeles)
	if position.distance_to(destino_actual) < 3.0:
		print("vamos no movimos 😍")
		
		enviar_nodo.emit(nodo_actual_nombre)
		
		#nos frenamos para que python verifique si la calle esta bloqueada
		viajando = false
		print("python necesitamos hablar 💀")

func establecer_objetivo(coords: Vector2, nombre: String) -> void:
	destino_actual = coords
	nodo_actual_nombre = nombre
	viajando = true
