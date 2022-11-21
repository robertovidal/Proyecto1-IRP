import cv2
import easyocr
import os

# Se van a utilizar 785 especímenes de cada número
# Los especímenes están en esta carpeta:
# https://drive.google.com/drive/folders/1qTAt09H2X3dENsdTwr7O5GL1X8xTymgL?usp=sharing

# Se uitila el 100% de especímenes para pruebas.
# Son 785 por número, en total 7850.
especimenes_prueba = []
for i in range(10):
    especimenes_prueba.append([])
    for j in range(785):
        especimen = cv2.imread("Especimenes/"+str(i)+"/especimen_"+str(j)+".jpg")
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