import importlib

def barrer(instrumento, canales):
    a_numero = importlib.import_module("02_magnitudes").a_numero
    config_magnitudes = [
        ("FREQuency", "FREQ", "Hz"),
        ("PKPK", "PKPK", "V"),
        ("CYCRms", "CYCRMS", "V")
    ]
    resultados = []
    for canal in canales:
        for comando_mag, nombre_mag, unidad in config_magnitudes:
            comando = f":MEASUrement:{canal}:{comando_mag}?"
            respuesta_cruda = instrumento.preguntar(comando)
            valor_num = a_numero(respuesta_cruda)
            resultados.append({
                "canal": canal,
                "magnitud": nombre_mag,
                "unidad": unidad,
                "texto_crudo": respuesta_cruda,
                "valor_convertido": valor_num
            })
    return resultados

if __name__ == '__main__':
    class InstrumentoDeMentira:
        def preguntar(self, comando):
            if "CH3" in comando:
                return "ERROR: comando desconocido"
            return "1.000000E+03"

    instrumento_mock = InstrumentoDeMentira()
    mediciones = barrer(instrumento_mock, ["CH1", "CH2"])
    assert len(mediciones) == 6
    assert mediciones[0]["canal"] == "CH1"
    assert mediciones[0]["magnitud"] == "FREQ"
    assert mediciones[0]["unidad"] == "Hz"
    assert mediciones[0]["texto_crudo"] == "1.000000E+03"
    assert mediciones[0]["valor_convertido"] == 1000.0
    
    mediciones_rotas = barrer(instrumento_mock, ["CH3"])
    assert mediciones_rotas[0]["texto_crudo"] == "ERROR: comando desconocido"
    assert mediciones_rotas[0]["valor_convertido"] is None
    print("pruebas OK")
