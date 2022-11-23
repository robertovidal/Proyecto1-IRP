# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2
from random import seed
from random import shuffle
import time
import os
from Entrenamiento import crear_modelo
from Entrenamiento import calcular_momentos_hu

# Esta función devuelve el resultado de la imagen
# es decir devuelve qué numero es, esto a partir de
# la imagen y los promedios y las varianzas de los
# momentos Hu de los números.
def reconocedor_numeros(imagen, promedios, varianzas):
    # Se generan los momentos Hu de la imagen
    valores_hu = calcular_momentos_hu(imagen)
    numero_escogido = -1
    aprobadas_numero_escogido = 0
    diferencias_numero_escogido = 0
    for i in range(len(promedios)):
        aprobadas = 0
        diferencias = 0
        # Se recorren los valores Hu comparándolos
        # con el promedio y la varianza de los valores Hu
        # de los números
        for j in range(len(valores_hu)):
            # Se calcula la diferencia al cuadrado respecto al
            # promedio del número
            diferencia = (valores_hu[j] - promedios[i][j]) ** 2
            diferencias += diferencia
            # Si el valor de la diferencia es menor o igual a
            # la varianza se dice que se aprueba
            if diferencia <= varianzas[i][j]:
                aprobadas += 1
        # Si se aprueban más de 3 valores Hu
        # y el valor de aprobadas es mayor al del número
        # escogido anteriormente, se escoge este número
        if aprobadas >= 3 and aprobadas > aprobadas_numero_escogido:
            numero_escogido = i
            aprobadas_numero_escogido = aprobadas
            diferencias_numero_escogido = diferencias
        # Si se aprueban más de 10 valores Hu
        # y el valor de aprobadas es igual al del número
        # escogido anteriormente, pero las diferencias 
        # encontradas son menores al del número escogido
        # se escoge este número.
        elif aprobadas >= 3 and aprobadas == aprobadas_numero_escogido and diferencias < diferencias_numero_escogido:
            numero_escogido = i
            aprobadas_numero_escogido = aprobadas
            diferencias_numero_escogido = diferencias
    return numero_escogido

# Se van a utilizar 785 especímenes de cada número
# por lo que el 70% de estos serían 550.
# Los especímenes están en esta carpeta:
# https://drive.google.com/drive/folders/1qTAt09H2X3dENsdTwr7O5GL1X8xTymgL?usp=sharing
seed(time.time())
# Se realiza una lista con los números del 0 al 784
posiciones = [i for i in range(785)]
# Se realiza un shuffle a la lista, para conseguir
# posiciones aleatorias.
shuffle(posiciones)

# Las posiciones de entrenamiento, que son el 70%
# van del 0 al 549
posiciones_entrenamiento = posiciones[0:550]
# El resto de posiciones son para pruebas.
posiciones_pruebas = posiciones[551:785]

# A partir de estas posiciones se cargan los
# especímenes correspondientes.
especimenes_entrenamiento = []
especimenes_prueba = []
for i in range(10):
    especimenes_entrenamiento.append([])
    for j in posiciones_entrenamiento:
        especimen = cv2.imread("Especimenes/"+str(i)+"/especimen_"+str(j)+".jpg")
        especimenes_entrenamiento[i].append(especimen)
    especimenes_prueba.append([])
    for j in posiciones_pruebas:
        especimen = cv2.imread("Especimenes/"+str(i)+"/especimen_"+str(j)+".jpg")
        especimenes_prueba[i].append(especimen)

# Se cargan los promedios y las varianzas de los momentos Hu
# utilizando los especímenes de entrenamiento
promedios_momentos_hu, varianzas_momentos_hu = crear_modelo(especimenes_entrenamiento)

# Se guardan los promedio y las varianzas obtenidas
# en un txt
try:
    os.remove("promedios_numeros.txt")
except OSError:
    pass
f = open("promedios_numeros.txt", "a")

for i in range(10):
    f.write(str(promedios_momentos_hu[i]) + "\n")

f.close()
try:
    os.remove("varianzas_numeros.txt")
except OSError:
    pass
f = open("varianzas_numeros.txt", "a")

for i in range(10):
    f.write(str(varianzas_momentos_hu[i]) + "\n")

f.close()

correctos = 0
incorrectos = 0

correctos_numeros = [0,0,0,0,0,0,0,0,0,0]
incorrectos_numeros = [0,0,0,0,0,0,0,0,0,0]
falsos_positivos = [0,0,0,0,0,0,0,0,0,0]

# Se realizan las pruebas con los especímenes de prueba
# y se calculan cuales fueron predicciones correctas
# e incorrectas
for i in range(10):
    for especimen in especimenes_prueba[i]:
        resultado = reconocedor_numeros(especimen, promedios_momentos_hu, varianzas_momentos_hu)
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