# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import sys
import os
actual = os.path.dirname(os.path.realpath(__file__))
actual = os.path.dirname(actual)
actual = os.path.dirname(actual)
sys.path.append(actual)
from Pruebas_General import Pruebas
from Cargar import cargar_especimenes_internet

pruebas = Pruebas(500, "Momentos Hu")
pruebas.cargar_especimenes(cargar_especimenes_internet)
pruebas.crear_modelo()
pruebas.guardar_promedios_varianzas()
pruebas.obtener_resultados(3)
pruebas.guardar_resultados()