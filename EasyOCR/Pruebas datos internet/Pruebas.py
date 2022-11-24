# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2
import easyocr

img = cv2.imread('digits.png')

w, h = img.shape[:2]
#preprocesamiento
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

# Dividimos la imagen en 5 mil (50x100) parches de 20x20 cada uno
especimenes = [thresh[x:x+20,y:y+20] for x in range(0,thresh.shape[0],20) for y in range(0,thresh.shape[1],20)]

especimenes_prueba = []
for i in range(10):
    especimenes_prueba.append([])
    for j in range(500):
        posicion_especimen = i * 499 + j
        especimen = especimenes[posicion_especimen]
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
