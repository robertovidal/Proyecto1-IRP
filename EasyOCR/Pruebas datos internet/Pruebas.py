# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2
import easyocr
import os

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
        resultado = reader.readtext(especimen, paragraph=False)
        if len(resultado) == 1:
            try:
                resultado = int(resultado[0][1])
                if resultado == i:
                    correctos+=1
                    correctos_numeros[i]+=1
                else:
                    incorrectos+=1
                    incorrectos_numeros[i]+=1
                    falsos_positivos[resultado]+=1
            except:
                    incorrectos += 1
                    incorrectos_numeros[i]+=1

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