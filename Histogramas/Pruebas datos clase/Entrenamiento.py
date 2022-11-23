# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
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

# Esta función es para crear el modelo, es decir
# calcular el promedio y las varianzas de los histogramas
#a partir de los especímenes que se manden de entrada
def crear_modelo(especimenes):

    histogramas_especimenes  = [[],[],[],[],[],[],[],[],[],[]]
    suma_histogramas = [[],[],[],[],[],[],[],[],[],[]]

    # Se generan los histogramas de los especímenes y de paso
    # se calcula la suma de estos histogramas según cada número
    # para calcular el promedio
    for i in range(10):
        for especimen in especimenes[i]:
            histograma = generarHistograma(4, especimen, np.array([255,255,255]))
            histogramas_especimenes[i].append(histograma)
        suma_histogramas[i] = [sum(x) for x in zip(*histogramas_especimenes[i])]

    promedios_histogramas = [[],[],[],[],[],[],[],[],[],[]]

    # Se divide el resultado de estas sumas entre la cantidad de 
    # histogramas de cada número para encontrar el promedio
    for i in range(10):
        for j in range(len(suma_histogramas[i])):
            promedios_histogramas[i].append(suma_histogramas[i][j] / len(histogramas_especimenes[i]))

    varianzas_histogramas = [[],[],[],[],[],[],[],[],[],[]]

    # Se realiza la suma de las varianzas de los histogramas
    for i in range(10):
        for histograma in histogramas_especimenes[i]:
            for j in range(len(histograma)):
                if len(varianzas_histogramas[i]) < j + 1:
                    varianzas_histogramas[i].append(0)
                varianzas_histogramas[i][j] += (histograma[j] - promedios_histogramas[i][j]) ** 2
    
    # Finalmente se divide esta suma entre la cantidad de 
    # histograma para calcular la varianza.
    for i in range(10):
        for j in range(len(suma_histogramas[i])):
            varianzas_histogramas[i][j] = varianzas_histogramas[i][j] / len(histogramas_especimenes[i])
    
    return promedios_histogramas, varianzas_histogramas