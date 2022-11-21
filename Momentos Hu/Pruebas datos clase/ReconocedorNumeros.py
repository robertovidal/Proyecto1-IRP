from MomentosHu import calcular_momentos_hu

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