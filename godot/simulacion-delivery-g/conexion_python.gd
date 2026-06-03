extends Node

#creamos las instacias del cliente en godot
var socket = WebSocketPeer.new()
var url = "ws://localhost:8765"
var conectado = false

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
			#enviar_arrancar_moto()
			
			#tambien nos aseguramos que estamos recibiendo informacion desde python
			while socket.get_available_packet_count() > 0:
				var paquete = socket.get_packet()
				var ver_mensaje = paquete.get_string_from_utf8()
				#_manejo_datos(ver_mensaje)
				
	elif estado == WebSocketPeer.STATE_CLOSED:
		if conectado:
			#cerrando conexion
			conectado = false
	
