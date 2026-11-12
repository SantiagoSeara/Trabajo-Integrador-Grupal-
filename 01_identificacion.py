def parsear_idn(respuesta):
    if not respuesta:
        return None
    campos = respuesta.split(',')
    if len(campos) < 4:
        return None
    return {
        "fabricante": campos[0].strip(),
        "modelo": campos[1].strip(),
        "serie": campos[2].strip(),
        "version": campos[3].strip()
    }

if __name__ == '__main__':
    assert parsear_idn("OWON, ADS3202, 25470803, V1.2.0") == {
        "fabricante": "OWON", "modelo": "ADS3202", "serie": "25470803", "version": "V1.2.0"
    }
    assert parsear_idn(" OWON , XDM1041,25470803,V4.4.0,3 ") == {
        "fabricante": "OWON", "modelo": "XDM1041", "serie": "25470803", "version": "V4.4.0"
    }
    assert parsear_idn("") is None
    assert parsear_idn("OWON, ADS3202,254") is None
    assert parsear_idn("ERROR: comando desconocido") is None
    print("pruebas OK")
