# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2
import easyocr

# Se van a utilizar 785 especímenes de cada número
# Los especímenes están en esta carpeta:
# https://drive.google.com/drive/folders/1qTAt09H2X3dENsdTwr7O5GL1X8xTymgL?usp=sharing

# Se utiliza el 100% de especímenes para pruebas.
# Son 785 por número, en total 7850.
especimenes_prueba = []
for i in range(10):
    especimenes_prueba.append([])
    for j in range(785):
        especimen = cv2.imread("Especimenes/"+str(i)+"/especimen_"+str(j)+".jpg")
        especimenes_prueba[i].append(especimen)

reader = easyocr.Reader(["es"], gpu=True)

# Como la función para los resultados está en otra carpeta nos cambiamos
# de esta manera
import sys
import os
actual = os.path.dirname(os.path.realpath(__file__))
actual = os.path.dirname(actual)
sys.path.append(actual)
from Resultados import resultados
# Se obtienen los resultados
correctos, incorrectos, correctos_numeros, incorrectos_numeros, falsos_positivos = resultados(especimenes_prueba, reader)

# Aquí también nos cambiamos de carpeta
actual = os.path.dirname(actual)
sys.path.append(actual)
from Guardar import guardar_resultados
# Se guardan los resultados
guardar_resultados(correctos, incorrectos, correctos_numeros,incorrectos_numeros,falsos_positivos)