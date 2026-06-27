extends Node2D
class_name InterfazLogitica

#creamos la señal que recibira nuertros controlador principal
signal destino_seleccionado(destino: String)
@onready var nodo_actual = $CanvasLayer/MarginContainer/PanelContainer/MarginContainer/VBoxContainer/HBoxContainer3/Label
@onready var velocidad = $CanvasLayer2/DashboardMoto/MarginContainer/VBoxContainer/Label2
@onready var distacia = $CanvasLayer2/DashboardMoto/MarginContainer/VBoxContainer/Label3
@onready var tiempo = $CanvasLayer2/DashboardMoto/MarginContainer/VBoxContainer/Label4
@onready var ruta = $CanvasLayer2/DashboardMoto/MarginContainer/VBoxContainer/Label5
@onready var progreso = $CanvasLayer2/DashboardMoto/MarginContainer/VBoxContainer/Progress_Ruta
@onready var estado = $CanvasLayer/MarginContainer/PanelContainer/MarginContainer/VBoxContainer/HBoxContainer2/Label

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

func _on_actualizar_interfaz(info: Dictionary):
	#aqui actualizamos la interfaz con los llamo de controlador
	match info.get("Tipo"):
		"Datos_Generales":
			var estado_acomodado = str(info["Estado"])
			estado.text = "Estado: " + estado_acomodado.replace("_", " ")
			distacia.text = "Distancia: " + str(info["Distancia"]) + " km"
			tiempo.text = "Tiempo: " + str(info["Tiempo"]) + " min"
			var nombres_limpios = []
			for nodo in info["Ruta_Completa_Dijkstra"]:
				var nombre_acomodado = nodo.replace("_", " ")
				nombres_limpios.append(nombre_acomodado)
			var ruta_acomodada = " -> ".join(nombres_limpios)
			
			ruta.text = "Ruta: " + ruta_acomodada
		"Nodo1":
			nodo_actual.text = "siguiente nodo: " + str(info["Siguiente_Nodo"])
		"Velocidad":
			print("verga que hola alv")
			velocidad.text = "Velocidad: " + str(info["Valor"]) + " km/h"
		"Progreso":
			progreso.value = info["Valor"] * 100
		"Actualizar_Estado":
			var estado_acomodado = str(info["Estado"])
			estado.text = "Estado: " + estado_acomodado.replace("_", " ")

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
