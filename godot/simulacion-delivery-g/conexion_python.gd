extends Node

#creamos las instacias del cliente en godot
var socket = WebSocketPeer.new()
var url = "ws://localhost:8765"
var conectado = false
signal ruta_python(evento: String, datos: Dictionary)

func _ready() -> void:
	#aqui es donde vamos a hacer la conexion(basicamente una llamada a python)
	var error = socket.connect_to_url(url)
	
	if error != OK:
		#aqui es donde la conexion se corta y dejamos de enviar informacion por el puerto
		set_process(false)

#aqui verificamos los procesos de la conexion
func _process(_delta) -> void:
	socket.poll()
	
	var  estado = socket.get_ready_state()
	
	if estado == WebSocketPeer.STATE_OPEN:
		if not conectado:
			#una vez hechas la verificaciones estamos conectados con python
			conectado = true
			#mandamos a arrancar la moto dentro de python
			enviar_arranque_moto()
			
			#tambien nos aseguramos que estamos recibiendo informacion desde python
			while socket.get_available_packet_count() > 0:
				var paquete = socket.get_packet()
				var ver_mensaje = paquete.get_string_from_utf8()
				_manejar_datos(ver_mensaje)
				
	elif estado == WebSocketPeer.STATE_CLOSED:
		if conectado:
			#cerrando conexion
			conectado = false
			
#enviamos el comando para ir encendiendo la moto
func enviar_arranque_moto() -> void:
	#la peticion deberia ser exactamente como python lo esta esperando
	var peticion = {
		"Comando": "Arrancar_Moto",
		"Moto": {
			"Id_Moto": "moto_01",
			"Destino": "Maraven"
		}
	}
	
	#lo convertimos en json para enviarse lo a python
	var arranque_moto_json = JSON.stringify(peticion)
	
	socket.send_text(arranque_moto_json)

#ahora que tenemos todo preparado, nos encargamos de enviar y recibir informacion
func _manejar_datos(text: String) -> void:
	#creamos un un archivo json para desempaquetar la inforfacion del python
	var json = JSON.new()
	#ahora creamos una nueva variable por si ocurre un error
	var error_json = json.parse(text)
	
	if error_json == OK:
		var respuesta = json.get_data() as Dictionary
		
		#ahora hacemos la verificaciones de acuerdo a los eventos 
		if respuesta.get("Evento") == "Moto_en_Camino":
			#extraemos la ruta que ya calculo dijkstra para hacer referencia a ella en el mapa
			var nombre_evento = respuesta.get("Evento")
			ruta_python.emit(nombre_evento, respuesta)
			
		elif respuesta.get("Evento") == "Moto_en_Camino":
			#ahora extraemos lo que serian los puntos a los que se tiene que dirijir la moto
			print("estado de la moto: ", respuesta["Datos"]["Estado"])
		
	else:
		print("error al pasar los datos del python")
