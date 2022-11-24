# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2
import numpy as np

def generarHistograma(pixeles, imagen, color):
  # se divide la cantidad de pixeles entre
  # porque la cantidad corresponde a un cuadrado
  # entonces si es 4 debemos hacer cada 2 filas
  # y cada 2 columnas
  pixeles = pixeles//2
  w, h = imagen.shape[:2]
  matrizHistograma = np.zeros([w//pixeles,h//pixeles], dtype=int)

  for x in range(0,w,pixeles):
    for y in range(0,h,pixeles):
      totPixeles = 0
      # aquí se cuenta la cantidad de pixeles
      # que corresponden al color que se envía
      # en el espacio de pixeles determinado
      for x2 in range(pixeles):
        for y2 in range(pixeles):
          if x+x2 < w and y+y2 < h:
            if np.array_equal(imagen[x+x2][y+y2], color):
              totPixeles += 1
      matrizHistograma[x//pixeles][y//pixeles] = totPixeles
  # numpy permite calcular la suma de columnas o filas
  # entonces aquí devolvemos el primer array es de las
  # filas y el segundo de las columnas
  horizontal = np.sum(matrizHistograma, axis=1)
  vertical = np.sum(matrizHistograma, axis=0)
  return np.concatenate((horizontal, vertical))


# En esta función se calculan los mentos de Hu de
# una imagen
def calcular_momentos_hu(imagen):
  imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  
  _,imagen = cv2.threshold(imagen, 128, 255, cv2.THRESH_BINARY)
  momentos = cv2.moments(imagen) 
  momentosHu = cv2.HuMoments(momentos)
  momentosHu = np.asarray(momentosHu).reshape(-1)
  return momentosHu

# Esta función es para crear el modelo, es decir
# calcular el promedio y las varianzas de los momentos Hu
#a partir de los especímenes que se manden de entrada
def crear_modelo(especimenes, tipo):

    especimenes_evaluados  = [[],[],[],[],[],[],[],[],[],[]]
    suma_especimenes = [[],[],[],[],[],[],[],[],[],[]]

    # Se generan los momentos Hu de los especímenes y de paso
    # se calcula la suma de estos momentos Hu según cada número
    # para calcular el promedio
    for i in range(10):
        for especimen in especimenes[i]:
            if tipo == "Histogramas":
                valores = generarHistograma(4, especimen, np.array([255,255,255]))
            elif tipo == "Momentos Hu":
                valores = calcular_momentos_hu(especimen)
            else:
                raise Exception("Solo se aceptan los valores Histogramas o Momentos Hu para el tipo del reconocedor")
            especimenes_evaluados[i].append(valores)
        suma_especimenes[i] = [sum(x) for x in zip(*especimenes_evaluados[i])]

    promedios_especimenes = [[],[],[],[],[],[],[],[],[],[]]

    # Se divide el resultado de estas sumas entre la cantidad de 
    # momentos Hu de cada número para encontrar el promedio
    for i in range(10):
        for j in range(len(suma_especimenes[i])):
            promedios_especimenes[i].append(suma_especimenes[i][j] / len(especimenes_evaluados[i]))

    varianzas_momentos_hu = [[],[],[],[],[],[],[],[],[],[]]

    # Se realiza la suma de las varianzas de los momentos Hu
    for i in range(10):
        for especimen in especimenes_evaluados[i]:
            for j in range(len(especimen)):
                if len(varianzas_momentos_hu[i]) < j + 1:
                    varianzas_momentos_hu[i].append(0)
                varianzas_momentos_hu[i][j] += (especimen[j] - promedios_especimenes[i][j]) ** 2
    
    # Finalmente se divide esta suma entre la cantidad de 
    # momentos Hu para calcular la varianza.
    for i in range(10):
        for j in range(len(suma_especimenes[i])):
            varianzas_momentos_hu[i][j] = varianzas_momentos_hu[i][j] / len(especimenes_evaluados[i])
    
    return promedios_especimenes, varianzas_momentos_hu


    