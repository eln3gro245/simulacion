extends Node

#aqui hacemos la logica para no saturar nuestra funcion principal
#vamos a traducir las pocisiones (x,y) de  godot para el desplazamiento de la moto
func _convertir_ruta(lugar: Node, ruta: Array) -> Dictionary:
	print("llego la ruta vamos 😘")
	var nuevas_coordenadas: Array[Vector2] = []
	var los_nodos: Dictionary = {}
	
	for i in range(ruta.size() - 1):
		var nombre_origen = ruta[i]
		
		#buscamos el nodos actual en nuestra esena de godot
		var nodo_actual = lugar.get_node_or_null(nombre_origen)
		los_nodos[nuevas_coordenadas.size()] = nombre_origen
		
		if nodo_actual != null:
			print("las ruta estan guardadas rey")
			#ahora lo guardamos dentro de nuestras coordenadas
			nuevas_coordenadas.append(nodo_actual.global_position)
		else:
			print("verga rey no consegui los nodos 😭")
			print("❌ FALLO: El nodo '", nombre_origen, "' no existe en Entidades_Simulacion.")
		
		var nombre_destino = ruta[i+1]
		var nombre_carpeta = nombre_origen + "_a_" + nombre_destino
		var nombre_cruces = lugar.get_node_or_null("Cruces_Intermedios/"+ nombre_carpeta)
		if nombre_cruces:
			for cruce in nombre_cruces.get_children():
				los_nodos[nuevas_coordenadas.size()] = "Cruce"
				nuevas_coordenadas.append(cruce.global_position)
	
	var ultimo_nombre = ruta.back()
	var ultimo_elemento = lugar.get_node_or_null(ultimo_nombre)
	if ultimo_elemento:
		los_nodos[nuevas_coordenadas.size()] = ultimo_nombre
		nuevas_coordenadas.append(ultimo_elemento.global_position)
	return { "coordenadas": nuevas_coordenadas, "mapa": los_nodos }
	
	
