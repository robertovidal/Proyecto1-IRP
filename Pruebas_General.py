# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
from random import seed
from random import shuffle
import time
import cv2
import os
import numpy as np
from Entrenamiento import crear_modelo
from Entrenamiento import generarHistograma
from Entrenamiento import calcular_momentos_hu
from Guardar import guardar_resultados

class Pruebas:
    def __init__(self, cantidad, tipo):
        self.tipo = tipo
        setenta_porciento = round(cantidad * 0.7)
        seed(time.time())
        # Se realiza una lista con los números del 0 al que se haya indicado
        self.posiciones = [i for i in range(cantidad)]
        # Se realiza un shuffle a la lista, para conseguir
        # posiciones aleatorias.
        shuffle(self.posiciones)

        # Las posiciones de entrenamiento, que son el 70%
        self.posiciones_entrenamiento = self.posiciones[0:setenta_porciento]
        # El resto de posiciones son para pruebas.
        self.posiciones_pruebas = self.posiciones[setenta_porciento+1:cantidad]

        self.especimenes_entrenamiento = []
        self.especimenes_prueba = []

    def cargar_especimenes(self, cargar_func):
        cargar_func(self.posiciones_entrenamiento, self.especimenes_entrenamiento, self.posiciones_pruebas, self.especimenes_prueba)

    def guardar_promedios_varianzas(self):
        archivos = ["promedios_numeros.txt", "varianzas_numeros.txt"]
        # Se guardan los promedio y las varianzas obtenidas
        # en un txt
        for j in range(len(archivos)):
          try:
              os.remove(archivos[j])
          except OSError:
              pass
          f = open(archivos[j], "a")
          if j == 0:
            for i in range(9):
                f.write(str(self.promedios_histogramas[i]) + "\n")
            f.write(str(self.promedios_histogramas[9]))
          else:
            for i in range(9):
                f.write(str(self.varianzas_histogramas[i]) + "\n")
            f.write(str(self.varianzas_histogramas[9]))

          f.close()

    def crear_modelo(self):
        # Se cargan los promedios y las varianzas de los histogramas
        # utilizando los especímenes de entrenamiento
        self.promedios_histogramas, self.varianzas_histogramas = crear_modelo(self.especimenes_entrenamiento, self.tipo)

    # Esta función devuelve el resultado de la imagen
    # es decir devuelve qué numero es, esto a partir de
    # la imagen y los promedios y las varianzas de los
    # histogramas de los números.
    def reconocedor_numeros(self, imagen, promedios, varianzas, cant_aprobadas):
        # Se genera el histograma de la imagen
        if self.tipo == "Histogramas":
            valores = generarHistograma(4, imagen, np.array([255,255,255]))
        elif self.tipo == "Momentos Hu":
            valores = calcular_momentos_hu(imagen)
        else:
          raise Exception("Solo se aceptan los valores Histogramas o Momentos Hu para el tipo del reconocedor")
        numero_escogido = -1
        aprobadas_numero_escogido = 0
        diferencias_numero_escogido = 0
        for i in range(len(promedios)):
            aprobadas = 0
            diferencias = 0
            # Se recorren los valores del histograma comparándolo
            # con el promedio y la varianza de los histogramas
            # de los números
            for j in range(len(valores)):
                # Se calcula la diferencia al cuadrado respecto al
                # promedio del número
                diferencia = (valores[j] - promedios[i][j]) ** 2
                diferencias += diferencia
                # Si el valor de la diferencia es menor o igual a
                # la varianza se dice que se aprueba
                if diferencia <= varianzas[i][j]:
                    aprobadas += 1
            # Si se aprueban más de 10 valores del histograma
            # y el valor de aprobadas es mayor al del número
            # escogido anteriormente, se escoge este número
            if aprobadas >= cant_aprobadas and aprobadas > aprobadas_numero_escogido:
                numero_escogido = i
                aprobadas_numero_escogido = aprobadas
                diferencias_numero_escogido = diferencias
            # Si se aprueban más de 10 valores del histograma
            # y el valor de aprobadas es igual al del número
            # escogido anteriormente, pero las diferencias 
            # encontradas son menores al del número escogido
            # se escoge este número.
            elif aprobadas >= cant_aprobadas and aprobadas == aprobadas_numero_escogido and diferencias < diferencias_numero_escogido:
                numero_escogido = i
                aprobadas_numero_escogido = aprobadas
                diferencias_numero_escogido = diferencias
        return numero_escogido

    def obtener_resultados(self,cant_aprobadas):
        self.correctos = 0
        self.incorrectos = 0

        self.correctos_numeros = [0,0,0,0,0,0,0,0,0,0]
        self.incorrectos_numeros = [0,0,0,0,0,0,0,0,0,0]
        self.falsos_positivos = [0,0,0,0,0,0,0,0,0,0]

        # Se realizan las rpuebas con los especímenes de prueba
        # y se calculan cuales fueron predicciones correctas
        # e incorrectas
        for i in range(10):
            for especimen in self.especimenes_prueba[i]:
                resultado = self.reconocedor_numeros(especimen, self.promedios_histogramas, self.varianzas_histogramas, cant_aprobadas)
                if resultado == i:
                    self.correctos+=1
                    self.correctos_numeros[i]+=1
                else:
                    self.incorrectos+=1
                    self.incorrectos_numeros[i]+=1
                    self.falsos_positivos[resultado]+=1
    
    def guardar_resultados(self):
        guardar_resultados(self.correctos, self.incorrectos, self.correctos_numeros, self.incorrectos_numeros, self.falsos_positivos)

