extends Node2D
class_name InterfazLogitica

#creamos la señal que recibira nuertros controlador principal
signal destino_seleccionado(destino: String)

#esta es la variable que almacena el distino elegido pero no hace mas nada que guardarlo
var destino_final: String = ""

func _ready() -> void:
	print("activo papi")
#guardamos la variable cuando sea recibida
func _on_oprimir_boton(parada: String) -> void:
	print("mano aqui esta la parada")
	destino_final = parada
	
#ahora hacemos que lo que se escogio pueda ser validado
func _on_boton_recorrido_pressed() -> void:
	print("se presiono el boton")
	if destino_final == "":
		print("Seleccione una ruta para continuar")
	
	#enviamos la informacion del contenedor por la señal
	destino_seleccionado.emit(destino_final)


func _on_zona_franca_label_pressed() -> void:
	_on_oprimir_boton("Zona_Franca")


func _on_hosp_calle_sierra_label_pressed() -> void:
	_on_oprimir_boton("Hospital_Calle_Sierra")


func _on_punta_cardon_label_pressed() -> void:
	_on_oprimir_boton("Punta_Cardon")


func _on_centro_label_pressed() -> void:
	_on_oprimir_boton("Centro")


func _on_las_margaritas_label_pressed() -> void:
	_on_oprimir_boton("Las_Margaritas")


func _on_el_sabino_label_pressed() -> void:
	_on_oprimir_boton("Distribuidor_El_Sabino")


func _on_unefa_label_pressed() -> void:
	_on_oprimir_boton("UNEFA")


func _on_maraven_label_pressed() -> void:
	_on_oprimir_boton("Maraven")


func _on_comunidad_cardon_label_pressed() -> void:
	_on_oprimir_boton("Comunidad_Cardon")


func _on_la_puerta_label_pressed() -> void:
	_on_oprimir_boton("La_Puerta")


func _on_button_pressed() -> void:
	_on_boton_recorrido_pressed()
