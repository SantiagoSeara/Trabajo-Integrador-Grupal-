from 02_magnitudes import a_numero

def barrer(instrumento, canales):
    """Pide al instrumento las 3 magnitudes por cada canal y devuelve la lista de resultados."""
    # Tupla con: (Comando SCPI, Nombre corto para tu diccionario/log, Unidad)
    config_magnitudes = [
        ("FREQuency", "FREQ", "Hz"),
        ("PKPK", "PKPK", "V"),
        ("CYCRms", "CYCRMS", "V")
    ]
    
    resultados = []
    
    for canal in canales:
        for comando_mag, nombre_mag, unidad in config_magnitudes:
            # Armamos el comando concatenando el canal y la magnitud[cite: 10, 11]
            comando = f":MEASUrement:{canal}:{comando_mag}?"
            
            # Le pedimos el dato al instrumento que nos pasaron por parámetro
            respuesta_cruda = instrumento.preguntar(comando)
            
            # Convertimos el texto usando tu función del ejercicio 2[cite: 10]
            # Si respuesta_cruda es un error del equipo, a_numero devolverá None automáticamente
            valor_num = a_numero(respuesta_cruda)
            
            resultados.append({
                "canal": canal,
                "magnitud": nombre_mag,
                "unidad": unidad,
                "texto_crudo": respuesta_cruda,
                "valor_convertido": valor_num
            })
            
    return resultados

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Escribimos la clase chiquita, de mentira, para probar sin prender el instrumento[cite: 11]
class InstrumentoDeMentira:
    def preguntar(self, comando):
        # Si le pedimos un canal que no existe, simulamos un error del equipo
        if "CH3" in comando:
            return "ERROR: comando desconocido"
        # Si está todo bien, devolvemos siempre este mismo número de mentira[cite: 11]
        return "1.000000E+03"

instrumento_mock = InstrumentoDeMentira()

# Prueba 1: Barrido de dos canales tiene que devolver exactamente 6 mediciones[cite: 11]
mediciones = barrer(instrumento_mock, ["CH1", "CH2"])
assert len(mediciones) == 6

# Prueba 2: Verificamos que el diccionario tenga la estructura exacta y el valor convertido[cite: 10]
primera = mediciones[0]
assert primera["canal"] == "CH1"
assert primera["magnitud"] == "FREQ"
assert primera["unidad"] == "Hz"
assert primera["texto_crudo"] == "1.000000E+03"
assert primera["valor_convertido"] == 1000.0

# Prueba 3: Si el instrumento contesta un error, el valor queda en None pero el texto crudo se guarda igual[cite: 11]
mediciones_rotas = barrer(instrumento_mock, ["CH3"])
assert mediciones_rotas[0]["texto_crudo"] == "ERROR: comando desconocido"
assert mediciones_rotas[0]["valor_convertido"] is None

print("pruebas OK")