import math

def vrms_teorico(vpp):
    if vpp is None or vpp < 0:
        return None
    vp = vpp / 2.0
    return vp / math.sqrt(2)

def coincide(medido, teorico, tolerancia=0.02):
    if medido is None or teorico is None or teorico == 0.0:
        return False
    error = abs(medido - teorico) / abs(teorico)
    return error <= tolerancia

def verificar_canal(filas, canal):
    vpp_medido = None
    vrms_medido = None
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

if __name__ == '__main__':
    assert coincide(0.71, vrms_teorico(2.0)) is True
    assert coincide(1.0, vrms_teorico(2.0)) is False
    
    barrido_simulado = [
        {"canal": "CH1", "magnitud": "FREQ", "valor_convertido": 1000.0},
        {"canal": "CH1", "magnitud": "PKPK", "valor_convertido": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "valor_convertido": 0.705}
    ]
    resultado = verificar_canal(barrido_simulado, "CH1")
    assert resultado["canal"] == "CH1"
    assert resultado["coincide"] is True
    assert coincide(None, 0.707) is False
    assert vrms_teorico(None) is None
    print("pruebas OK")
