import math

def a_numero(texto):
    try:
        v = float(texto)
    except (ValueError, TypeError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v

def con_unidad(valor, unidad):
    if valor == 0.0:
        return f"0 {unidad}"
        
    es_negativo = valor < 0
    v_abs = abs(valor)
    
    prefijos = [(1e9, 'G'), (1e6, 'M'), (1e3, 'k'), (1e0, ''), (1e-3, 'm'), (1e-6, 'u'), (1e-9, 'n'), (1e-12, 'p')]
    
    for factor, prefijo in prefijos:
        v_escalado = v_abs / factor
        v_redondeado = round(v_escalado, 3)
        if 1.0 <= v_redondeado < 1000.0:
            if v_redondeado.is_integer():
                resultado = str(int(v_redondeado))
            else:
                resultado = str(v_redondeado)
            signo = "-" if es_negativo else ""
            if prefijo == '':
                return f"{signo}{resultado} {unidad}"
            else:
                return f"{signo}{resultado} {prefijo}{unidad}"
    return f"{valor} {unidad}"

if __name__ == '__main__':
    assert a_numero("1.000000E+03") == 1000.0
    assert a_numero("-2.5E-03") == -0.0025
    assert a_numero("ERROR") is None
    assert a_numero(None) is None
    assert con_unidad(1000.0, "Hz") == "1 kHz"
    assert con_unidad(2500.0, "Hz") == "2.5 kHz"
    assert con_unidad(2.0, "V") == "2 V"
    assert con_unidad(0.707, "V") == "707 mV"
    assert con_unidad(0.0005, "s") == "500 us"
    assert con_unidad(999.9999, "Hz") == "1 kHz"
    assert con_unidad(0.0, "V") == "0 V"
    print("pruebas OK")
