# Copyright (C) 2022  Jose Blanco, Pablo Fernández, Jose Ocampo, Roberto Vidal

# No se pudo usar la clase que hicimos de pruebas generales
# porque los resultados de EasyOCR son muy distintos a los
# que se usan para las pruebas de los otros métodos

def resultados(especimenes_prueba, reader):
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
    return correctos, incorrectos, correctos_numeros, incorrectos_numeros, falsos_positivos