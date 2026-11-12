def parsear_idn(respuesta): #Se define la función para procesar el "instrumento de medición"  a un comando estándar (cómo un *IDN?)
    respuesta = respuesta.strip() #Línea que elimina los espacios y caracteres vacíos en la respuesta
    if respuesta.startswith("ERROR:"): #Comprueba que la información ingresada comience con el texto "error", si es así, corta y devuelve None (línea 4)
        return None #Si la condición es True en línea 3 devuelve un None.
        
    campos = respuesta.split(",") # Divide la respuesta en una lista separada por comas. El resultado se guarda en campos
    if len(campos) not in (4, 5): # Comprueba se la cantidad de elementos de la lista campos es diferente de 4 y 5 (normalmente se usa este rango)
        return None # Si no cumple con el requisito de línea 7, devuelve un None

    fabricante, modelo, serie, version = [
        campo.strip() for campo in campos[:4]
    ] # Las dos líneas de arriba asignan los primeros 4 elementos procesados detallados en L10. 
    if not all((fabricante, modelo, serie, version)): #Si no cumple con los parámetros detallados arriba, devuelve None. En caso de cumplir con todo (all()), continúa corriendo
        return None

    return {
        "fabricante": fabricante,
        "modelo": modelo,
        "serie": serie,
        "version": version,
    } # La función desde L16 a L21 devuelve un valor a cada variable (Ej: Fabricante = Motorola)


if __name__ == "__main__": #Este bloque sólo se ejecuta si el archivo corre como script, no como módulo de otro script
    # Respuesta del osciloscopio.
    assert parsear_idn("OWON,ADS3202,25470803,V1.2.0") == {
        "fabricante": "OWON",
        "modelo": "ADS3202",
        "serie": "25470803",
        "version": "V1.2.0",
    }

    # Respuesta del multímetro con espacios y un quinto campo.
    assert parsear_idn(" OWON , XDM1041 , 25470803 , V4.4.0 , 3 ") == {
        "fabricante": "OWON",
        "modelo": "XDM1041",
        "serie": "25470803",
        "version": "V4.4.0",
    }

    # Respuestas inválidas.
    assert parsear_idn("OWON,ADS3202,25470803") is None
    assert parsear_idn("") is None
    assert parsear_idn("ERROR: comando desconocido") is None

    print("pruebas OK")
    print(parsear_idn("OWON,ADS3202,25470803,V1.2.0"))
