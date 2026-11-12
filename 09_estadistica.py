import math

def resumen(valores):
    """Devuelve diccionario con n, minimo, maximo, promedio y desvio. None si está vacía."""
    if not valores:
        return None
        
    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n
    
    # Cálculo manual del desvío estándar muestral según fórmula de la cátedra[cite: 13]
    if n == 1:
        # Con un solo valor dividiríamos por cero, así que el desvío es 0.0[cite: 13]
        desvio = 0.0
    else:
        # Sumatoria de las diferencias al cuadrado
        suma_cuadrados = sum((v - promedio) ** 2 for v in valores)
        desvio = math.sqrt(suma_cuadrados / (n - 1))
        
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio
    }

def fuera_de_rango(valores, minimo, maximo):
    """Devuelve las posiciones (índices) de los valores que se salen del rango especificado."""
    posiciones = []
    # Usamos enumerate para tener el índice y el valor al mismo tiempo
    for i, v in enumerate(valores):
        # Los dos extremos del rango cuentan como adentro[cite: 13]
        if v < minimo or v > maximo:
            posiciones.append(i)
            
    return posiciones

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Pruebas de resumen()[cite: 13]
# 1. Caso límite: lista vacía
assert resumen([]) is None

# 2. Caso límite: lista con un solo valor (evita división por cero)
res_unico = resumen([10.0])
assert res_unico["n"] == 1
assert res_unico["desvio"] == 0.0
assert res_unico["promedio"] == 10.0

# 3. Caso normal: serie de prueba para verificar los cálculos matemáticos
res_normal = resumen([2.0, 4.0, 4.0, 4.5, 5.0, 5.0, 7.0, 9.0])
assert res_normal["n"] == 8
assert res_normal["minimo"] == 2.0
assert res_normal["maximo"] == 9.0
assert res_normal["promedio"] == 5.0625
# El desvío de esta muestra redondeado a 4 decimales es 2.1293
assert round(res_normal["desvio"], 4) == 2.1293

# Pruebas de fuera_de_rango()[cite: 13]
# 1. Los valores exactamente en los límites cuentan como adentro
assert fuera_de_rango([10, 15, 20], 10, 20) == []

# 2. Retorna las posiciones de los elementos que se salen del rango
assert fuera_de_rango([5, 15, 25, 10], 10, 20) == [0, 2] # Las posiciones 0 (valor 5) y 2 (valor 25)

print("pruebas OK")