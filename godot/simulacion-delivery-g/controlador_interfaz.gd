extends CanvasLayer
class_name InterfazLogitica

#creamos la señal que recibira nuertros controlador principal
signal destino_seleccionado(destino: String)

#esta es la variable que almacena el distino elegido pero no hace mas nada que guardarlo
var destino_final: String = ""

#guardamos la variable cuando sea recibida
func _on_oprimir_boton(parada: String) -> void:
	destino_final = parada
	

#ahora hacemos que lo que se escogio pueda ser validado
func _on_boton_recorrido_pressed() -> void:
	if destino_final == "":
		print("Seleccione una ruta para continuar")
	
	#enviamos la informacion del contenedor por la señal
	destino_seleccionado.emit(destino_final)
