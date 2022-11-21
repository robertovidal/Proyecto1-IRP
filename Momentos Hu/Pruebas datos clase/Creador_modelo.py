# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal
from MomentosHu import calcular_momentos_hu


# Esta función es para crear el modelo, es decir
# calcular el promedio y las varianzas de los momentos Hu
#a partir de los especímenes que se manden de entrada
def crear_modelo(especimenes):

    momentos_hu_especimenes  = [[],[],[],[],[],[],[],[],[],[]]
    suma_momentos_hu = [[],[],[],[],[],[],[],[],[],[]]

    # Se generan los momentos Hu de los especímenes y de paso
    # se calcula la suma de estos momentos Hu según cada número
    # para calcular el promedio
    for i in range(10):
        for especimen in especimenes[i]:
            momentos_hu = calcular_momentos_hu(especimen)
            momentos_hu_especimenes[i].append(momentos_hu)
        suma_momentos_hu[i] = [sum(x) for x in zip(*momentos_hu_especimenes[i])]

    promedios_momentos_hu = [[],[],[],[],[],[],[],[],[],[]]

    # Se divide el resultado de estas sumas entre la cantidad de 
    # momentos Hu de cada número para encontrar el promedio
    for i in range(10):
        for j in range(len(suma_momentos_hu[i])):
            promedios_momentos_hu[i].append(suma_momentos_hu[i][j] / len(momentos_hu_especimenes[i]))

    varianzas_momentos_hu = [[],[],[],[],[],[],[],[],[],[]]

    # Se realiza la suma de las varianzas de los momentos Hu
    for i in range(10):
        for momentos_hu in momentos_hu_especimenes[i]:
            for j in range(len(momentos_hu)):
                if len(varianzas_momentos_hu[i]) < j + 1:
                    varianzas_momentos_hu[i].append(0)
                varianzas_momentos_hu[i][j] += (momentos_hu[j] - promedios_momentos_hu[i][j]) ** 2
    
    # Finalmente se divide esta suma entre la cantidad de 
    # momentos Hu para calcular la varianza.
    for i in range(10):
        for j in range(len(suma_momentos_hu[i])):
            varianzas_momentos_hu[i][j] = varianzas_momentos_hu[i][j] / len(momentos_hu_especimenes[i])
    
    return promedios_momentos_hu, varianzas_momentos_hu