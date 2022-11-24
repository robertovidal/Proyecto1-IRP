# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import os
def guardar_resultados(correctos, incorrectos, correctos_numeros,incorrectos_numeros,falsos_positivos):
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