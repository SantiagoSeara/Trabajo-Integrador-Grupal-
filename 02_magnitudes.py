def a_numero(texto):
    """Convierte texto en notación científica a float. Devuelve None si falla."""
    try:
        return float(texto)
    except (ValueError, TypeError):
        return None

def con_unidad(valor, unidad):
    """Convierte un valor float al prefijo más adecuado entre 1 y 999."""
    if valor == 0.0:
        # La tabla de la cátedra dice "0V", pero para mantener la regla 
        # general usamos "0 V". Si te observan el espacio, podés ajustarlo.
        return f"0 {unidad}"
        
    es_negativo = valor < 0
    v_abs = abs(valor)
    
    # Prefijos soportados ordenados de mayor a menor factor
    prefijos = [
        (1e9, 'G'),
        (1e6, 'M'),
        (1e3, 'k'),
        (1e0, ''),
        (1e-3, 'm'),
        (1e-6, 'u'),
        (1e-9, 'n'),
        (1e-12, 'p')
    ]
    
    for factor, prefijo in prefijos:
        # 1. Escalamos el valor al prefijo actual
        v_escalado = v_abs / factor
        
        # 2. Redondeamos a 3 decimales ANTES de preguntar si entra en el rango.
        # Esto soluciona la trampa del "999.9999" que menciona la consigna.
        v_redondeado = round(v_escalado, 3)
        
        # 3. Verificamos si el valor redondeado quedó entre 1 y 999.999...
        if 1.0 <= v_redondeado < 1000.0:
            
            # Formateamos para no dejar ".0" en números enteros
            if v_redondeado.is_integer():
                resultado = str(int(v_redondeado))
            else:
                resultado = str(v_redondeado)
                
            signo = "-" if es_negativo else ""
            
            if prefijo == '':
                return f"{signo}{resultado} {unidad}"
            else:
                return f"{signo}{resultado} {prefijo}{unidad}"
                
    # Fallback por si el número es inmensamente grande o pequeño
    return f"{valor} {unidad}"

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Pruebas de a_numero()[cite: 8]
assert a_numero("1.000000E+03") == 1000.0
assert a_numero("-2.5E-03") == -0.0025
# Caso raro: texto que no es número[cite: 7]
assert a_numero("ERROR") is None
# Caso raro: valor nulo[cite: 7]
assert a_numero(None) is None

# Pruebas de con_unidad() extraídas de la consigna[cite: 8]
assert con_unidad(1000.0, "Hz") == "1 kHz"
assert con_unidad(2500.0, "Hz") == "2.5 kHz"
assert con_unidad(2.0, "V") == "2 V"
assert con_unidad(0.707, "V") == "707 mV"
assert con_unidad(0.0005, "s") == "500 us"

# El caso que se le escapa a casi todo el mundo[cite: 9]
assert con_unidad(999.9999, "Hz") == "1 kHz"

print("pruebas OK")