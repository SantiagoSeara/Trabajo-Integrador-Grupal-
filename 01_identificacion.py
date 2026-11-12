def parsear_idn(respuesta): #Se define la función para procesar el "instrumento de medición"  a un comando estándar (cómo un *IDN?)
    respuesta = respuesta.strip()
    if respuesta.startswith("ERROR:"):
        return None

    campos = respuesta.split(",")
    if len(campos) not in (4, 5):
        return None

    fabricante, modelo, serie, version = [
        campo.strip() for campo in campos[:4]
    ]
    if not all((fabricante, modelo, serie, version)):
        return None

    return {
        "fabricante": fabricante,
        "modelo": modelo,
        "serie": serie,
        "version": version,
    }


if __name__ == "__main__":
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
