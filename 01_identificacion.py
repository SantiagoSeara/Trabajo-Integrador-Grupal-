def parsear_idn(respuesta): #Evalúa si la cadena está vacía o es nula (None). Si no hay respuesta, corta la ejecución y devuelve None de inmediato.
    # EVIDENCIA: Se requiere devolver None ante cadenas vacías.
    if not respuesta:
        return None
        
    # Separamos la cadena por comas
    campos = respuesta.split(',') #El método .split(',') corta la cadena de texto cada vez que encuentra una coma, transformando el string crudo en una lista de elementos (ej: ["OWON", " ADS3202", ...]).
    
    # DIAGNÓSTICO: Si hay menos de 4 campos, la respuesta es inválida. 
    # Esto también filtra automáticamente la respuesta "ERROR: comando desconocido".
    if len(campos) < 4: #Valida que la lista tenga al menos 4 posiciones. Esto descarta silenciosamente mensajes como "ERROR: comando desconocido", ya que al no tener comas, su longitud es 1.
        return None
        
    # COMPROBÉ: El método strip() elimina los espacios en blanco sobrantes a los lados.
    # Al acceder solo del índice 0 al 3, se descarta automáticamente el quinto campo del multímetro.
    return {
        "fabricante": campos[0].strip(),
        "modelo": campos[1].strip(),
        "serie": campos[2].strip(),
        "version": campos[3].strip()
    } #.strip() elimina los espacios en blanco sobrantes al principio y al final de cada campo. Al acceder explícitamente desde el índice [0] al [3], descartamos automáticamente cualquier quinto campo adicional que devuelva el multímetro.

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Prueba 1: Osciloscopio normal (4 campos)
assert parsear_idn("OWON, ADS3202, 25470803, V1.2.0") == {
    "fabricante": "OWON", 
    "modelo": "ADS3202", 
    "serie": "25470803", 
    "version": "V1.2.0"
}

# Prueba 2: Multímetro (5 campos, el quinto se descarta) con espacios extra a los lados[cite: 8]
assert parsear_idn(" OWON , XDM1041,25470803,V4.4.0,3 ") == {
    "fabricante": "OWON", 
    "modelo": "XDM1041", 
    "serie": "25470803", 
    "version": "V4.4.0"
}

# Prueba 3: Caso raro - Cadena vacía[cite: 8]
assert parsear_idn("") is None

# Prueba 4: Caso raro - Respuesta incompleta (3 campos)[cite: 7]
assert parsear_idn("OWON, ADS3202,254") is None

# Prueba 5: Caso raro - Mensaje de error literal del instrumento[cite: 8]
assert parsear_idn("ERROR: comando desconocido") is None

print("pruebas OK")