import math

def resumen(valores):
    if not valores:
        return None
    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n
    if n == 1:
        desvio = 0.0
    else:
        suma_cuadrados = sum((v - promedio) ** 2 for v in valores)
        desvio = math.sqrt(suma_cuadrados / (n - 1))
    return {
        "n": n, "minimo": minimo, "maximo": maximo,
        "promedio": promedio, "desvio": desvio
    }

def fuera_de_rango(valores, minimo, maximo):
    posiciones = []
    for i, v in enumerate(valores):
        if v < minimo or v > maximo:
            posiciones.append(i)
    return posiciones

if __name__ == '__main__':
    assert resumen([]) is None
    res_unico = resumen([10.0])
    assert res_unico["n"] == 1
    assert res_unico["desvio"] == 0.0
    assert res_unico["promedio"] == 10.0
    
    res_normal = resumen([2.0, 4.0, 4.0, 4.5, 5.0, 5.0, 7.0, 9.0])
    assert res_normal["n"] == 8
    assert res_normal["minimo"] == 2.0
    assert res_normal["maximo"] == 9.0
    assert res_normal["promedio"] == 5.0625
    assert round(res_normal["desvio"], 4) == 2.1293
    
    assert fuera_de_rango([10, 15, 20], 10, 20) == []
    assert fuera_de_rango([5, 15, 25, 10], 10, 20) == [0, 2]
    print("pruebas OK")
