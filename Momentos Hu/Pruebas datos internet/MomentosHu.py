# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
import cv2
import numpy as np
# En esta función se calculan los mentos de Hu de
# una imagen
def calcular_momentos_hu(imagen):
  imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  
  _,imagen = cv2.threshold(imagen, 128, 255, cv2.THRESH_BINARY)
  momentos = cv2.moments(imagen) 
  momentosHu = cv2.HuMoments(momentos)
  momentosHu = np.asarray(momentosHu).reshape(-1)
  return momentosHu