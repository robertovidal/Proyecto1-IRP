# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2

def cargar_especimenes_clase(posiciones_entrenamiento, especimenes_entrenamiento, posiciones_pruebas, especimenes_prueba):
    # A partir de estas posiciones se cargan los
    # especímenes correspondientes.
    for i in range(10):
        especimenes_entrenamiento.append([])
        for j in posiciones_entrenamiento:
            especimen = cv2.imread("Especimenes/"+str(i)+"/especimen_"+str(j)+".jpg")
            especimenes_entrenamiento[i].append(especimen)
        especimenes_prueba.append([])
        for j in posiciones_pruebas:
            especimen = cv2.imread("Especimenes/"+str(i)+"/especimen_"+str(j)+".jpg")
            especimenes_prueba[i].append(especimen)

def cargar_especimenes_internet(posiciones_entrenamiento, especimenes_entrenamiento, posiciones_pruebas, especimenes_prueba):
    img = cv2.imread('digits.png')

    #preprocesamiento
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    # Dividimos la imagen en 5 mil parches de 20x20 cada uno
    especimenes = [thresh[x:x+20,y:y+20] for x in range(0,thresh.shape[0],20) for y in range(0,thresh.shape[1],20)]

    # A partir de estas posiciones se cargan los
    # especímenes correspondientes.
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