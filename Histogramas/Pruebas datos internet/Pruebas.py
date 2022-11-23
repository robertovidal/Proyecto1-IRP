# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
from random import seed
from random import shuffle
import time
import cv2
import os
import numpy as np
from Entrenamiento import crear_modelo
from Entrenamiento import generarHistograma

# Esta función devuelve el resultado de la imagen
# es decir devuelve qué numero es, esto a partir de
# la imagen y los promedios y las varianzas de los
# histogramas de los números.
def reconocedor_numeros(imagen, promedios, varianzas):
    # Se genera el histograma de la imagen
    histograma = generarHistograma(4, imagen, np.array([255,255,255]))
    numero_escogido = -1
    aprobadas_numero_escogido = 0
    diferencias_numero_escogido = 0
    for i in range(len(promedios)):
        aprobadas = 0
        diferencias = 0
        # Se recorren los valores del histograma comparándolo
        # con el promedio y la varianza de los histogramas
        # de los números
        for j in range(len(histograma)):
            # Se calcula la diferencia al cuadrado respecto al
            # promedio del número
            diferencia = (histograma[j] - promedios[i][j]) ** 2
            diferencias += diferencia
            # Si el valor de la diferencia es menor o igual a
            # la varianza se dice que se aprueba
            if diferencia <= varianzas[i][j]:
                aprobadas += 1
        # Si se aprueban más de 10 valores del histograma
        # y el valor de aprobadas es mayor al del número
        # escogido anteriormente, se escoge este número
        if aprobadas >= 3 and aprobadas > aprobadas_numero_escogido:
            numero_escogido = i
            aprobadas_numero_escogido = aprobadas
            diferencias_numero_escogido = diferencias
        # Si se aprueban más de 10 valores del histograma
        # y el valor de aprobadas es igual al del número
        # escogido anteriormente, pero las diferencias 
        # encontradas son menores al del número escogido
        # se escoge este número.
        elif aprobadas >= 3 and aprobadas == aprobadas_numero_escogido and diferencias < diferencias_numero_escogido:
            numero_escogido = i
            aprobadas_numero_escogido = aprobadas
            diferencias_numero_escogido = diferencias
    return numero_escogido

# Se van a utilizar 500 especímenes de cada número
# por lo que el 70% de estos serían 350.
seed(time.time())
# Se realiza una lista con los números del 0 al 499
posiciones = [i for i in range(500)]
# Se realiza un shuffle a la lista, para conseguir
# posiciones aleatorias.
shuffle(posiciones)

# Las posiciones de entrenamiento, que son el 70%
# van del 0 al 349
posiciones_entrenamiento = posiciones[0:350]
# El resto de posiciones son para pruebas.
posiciones_pruebas = posiciones[351:500]

img = cv2.imread('digits.png')

w, h = img.shape[:2]
#preprocesamiento
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

# Dividimos la imagen en 5 mil (50x100) parches de 20x20 cada uno
especimenes = [thresh[x:x+20,y:y+20] for x in range(0,thresh.shape[0],20) for y in range(0,thresh.shape[1],20)]

# A partir de estas posiciones se cargan los
# especímenes correspondientes.
especimenes_entrenamiento = []
especimenes_prueba = []
for i in range(10):
    especimenes_entrenamiento.append([])
    for j in posiciones_entrenamiento:
        posicion_especimen = i * 499 + j
        especimen = especimenes[posicion_especimen]
        especimenes_entrenamiento[i].append(especimen)
    especimenes_prueba.append([])
    for j in posiciones_pruebas:
        posicion_especimen = i * 499 + j
        especimen = especimenes[posicion_especimen]
        especimenes_prueba[i].append(especimen)

# Se cargan los promedios y las varianzas de los histogramas
# utilizando los especímenes de entrenamiento
promedios_histogramas, varianzas_histogramas = crear_modelo(especimenes_entrenamiento)

# Se guardan los promedio y las varianzas obtenidas
# en un txt
try:
    os.remove("promedios_numeros.txt")
except OSError:
    pass
f = open("promedios_numeros.txt", "a")

for i in range(9):
    f.write(str(promedios_histogramas[i]) + "\n")
f.write(str(promedios_histogramas[9]))

f.close()

try:
    os.remove("varianzas_numeros.txt")
except OSError:
    pass
f = open("varianzas_numeros.txt", "a")

for i in range(9):
    f.write(str(varianzas_histogramas[i]) + "\n")
f.write(str(varianzas_histogramas[9]))

f.close()

correctos = 0
incorrectos = 0

correctos_numeros = [0,0,0,0,0,0,0,0,0,0]
incorrectos_numeros = [0,0,0,0,0,0,0,0,0,0]
falsos_positivos = [0,0,0,0,0,0,0,0,0,0]

# Se realizan las rpuebas con los especímenes de prueba
# y se calculan cuales fueron predicciones correctas
# e incorrectas
for i in range(10):
    for especimen in especimenes_prueba[i]:
        resultado = reconocedor_numeros(especimen, promedios_histogramas, varianzas_histogramas)
        if resultado == i:
            correctos+=1
            correctos_numeros[i]+=1
        else:
            incorrectos+=1
            incorrectos_numeros[i]+=1
            falsos_positivos[resultado]+=1

# Se guardan los resultados en un txt

try:
    os.remove("Resultados.txt")
except OSError:
    pass
f = open("Resultados.txt", "a")
f.write("Predicciones correctas "+str(correctos)+"\n")
f.write("Predicciones incorrectas "+str(incorrectos)+"\n\n")
f.write("Predicciones segun cada numero:\n")

for i in range(10):
    f.write("\nNumero "+str(i)+":\n")
    f.write("Correctas: "+str(correctos_numeros[i]) + "\n")
    f.write("Incorrectas: "+str(incorrectos_numeros[i])+ "\n")
    f.write("Falsos positivos: "+str(falsos_positivos[i])+ "\n")

f.close()