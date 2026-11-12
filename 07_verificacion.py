import math

def vrms_teorico(vpp):
    """Calcula el Vrms esperado para una señal senoidal dado su Vpp."""
    # Si no hay medición o el valor es físicamente imposible, no tiene sentido
    if vpp is None or vpp < 0:
        return None
        
    vp = vpp / 2.0
    return vp / math.sqrt(2) # Fórmula de la cátedra: Vrms = Vp / raiz(2)[cite: 5]

def coincide(medido, teorico, tolerancia=0.02):
    """Devuelve True si el valor medido cae dentro de la tolerancia relativa del teórico."""
    # Si perdimos algún dato o el teórico es 0 (evita división por cero), no coinciden
    if medido is None or teorico is None or teorico == 0.0:
        return False
        
    # Cálculo del error relativo según la fórmula exacta de la consigna[cite: 11]
    error = abs(medido - teorico) / abs(teorico)
    
    return error <= tolerancia

def verificar_canal(filas, canal):
    """Busca PKPK y CYCRMS de un canal en el barrido y verifica si coinciden."""
    vpp_medido = None
    vrms_medido = None
    
    # Extraemos los valores del canal que nos pidieron
    for fila in filas:
        if fila["canal"] == canal:
            if fila["magnitud"] == "PKPK":
                vpp_medido = fila["valor_convertido"]
            elif fila["magnitud"] == "CYCRMS":
                vrms_medido = fila["valor_convertido"]
                
    teorico = vrms_teorico(vpp_medido)
    resultado_coincide = coincide(vrms_medido, teorico)
    
    return {
        "canal": canal,
        "vpp_medido": vpp_medido,
        "vrms_medido": vrms_medido,
        "vrms_teorico": teorico,
        "coincide": resultado_coincide
    }

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Prueba 1: Funcionamiento normal con la tolerancia por defecto (2%)
# Vpp = 2.0 -> Vrms teórico = 0.7071... Medimos 0.71, debería pasar.
assert coincide(0.71, vrms_teorico(2.0)) is True

# Prueba 2: LA PRUEBA QUE DEMUESTRA QUE LA PRUEBA SIRVE[cite: 12]
# Señal cuadrada: Vpp=2V, Vrms=1V. Tiene que devolver que NO coincide.
# Inyectamos el Vrms medido (1.0) y el teórico calculado a partir del Vpp (2.0)
assert coincide(1.0, vrms_teorico(2.0)) is False

# Prueba 3: Verificación de un canal completo simulando salida de barrer()
barrido_simulado = [
    {"canal": "CH1", "magnitud": "FREQ", "valor_convertido": 1000.0},
    {"canal": "CH1", "magnitud": "PKPK", "valor_convertido": 2.0},
    {"canal": "CH1", "magnitud": "CYCRMS", "valor_convertido": 0.705} # Dentro del 2% de 0.7071
]

resultado = verificar_canal(barrido_simulado, "CH1")
assert resultado["canal"] == "CH1"
assert resultado["coincide"] is True

# Prueba 4: Valores nulos si el instrumento tiró error en el barrido
assert coincide(None, 0.707) is False
assert vrms_teorico(None) is None

print("pruebas OK")