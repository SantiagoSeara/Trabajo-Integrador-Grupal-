import os
import importlib

def analizar_linea(linea):
    a_numero = importlib.import_module("02_magnitudes").a_numero
    linea_limpia = linea.strip()
    if not linea_limpia or linea_limpia.startswith('#'):
        return (None, None)
        
    campos = linea_limpia.split()
    if len(campos) != 6:
        return (None, "la que no tiene exactamente seis campos")
        
    try:
        h, m, s = campos[1].split(':')
        if not (0 <= int(h) < 24 and 0 <= int(m) < 60 and 0 <= int(s) < 60):
            return (None, "la de hora imposible")
    except ValueError:
        return (None, "la de hora imposible")
        
    if campos[3] not in ("CH1", "CH2"):
        return (None, "la de canal que no es CH1 ni CH2")
    if campos[4] not in ("FREQ", "PKPK", "CYCRMS"):
        return (None, "la de magnitud que no es FREQ, PKPK ni CYCRMS")
        
    valor = a_numero(campos[5])
    if valor is None:
        return (None, "la de valor que no se puede convertir a número")
        
    medicion = {
        "fecha": campos[0], "hora": campos[1], "equipo": campos[2],
        "canal": campos[3], "magnitud": campos[4], "valor": valor
    }
    return (medicion, None)

def leer_log(ruta):
    series = {}
    rechazos = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for num, linea in enumerate(archivo, 1):
            medicion, motivo = analizar_linea(linea)
            if medicion is None and motivo is None:
                continue
            if motivo is not None:
                rechazos.append({"linea": num, "motivo": motivo})
            else:
                clave = (medicion["equipo"], medicion["canal"], medicion["magnitud"])
                if clave not in series:
                    series[clave] = []
                series[clave].append(medicion["valor"])
    return series, rechazos

if __name__ == '__main__':
    assert analizar_linea("") == (None, None)
    assert analizar_linea("# Inicio de mediciones") == (None, None)
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ")[1] == "la que no tiene exactamente seis campos"
    assert analizar_linea("2026-09-08 25:61:00 ADS3202 CH1 FREQ 1E03")[1] == "la de hora imposible"
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH3 FREQ 1E03")[1] == "la de canal que no es CH1 ni CH2"
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 RUIDO 1E03")[1] == "la de magnitud que no es FREQ, PKPK ni CYCRMS"
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ ERROR")[1] == "la de valor que no se puede convertir a número"
    
    linea_tabulada = "2026-09-08\t09:14:02\tADS3202\tCH1\tFREQ\t1.000431E+03"
    medicion_ok, motivo = analizar_linea(linea_tabulada)
    assert motivo is None
    assert medicion_ok["valor"] == 1000.431
    
    ruta_test = "test_temp.log"
    with open(ruta_test, "w") as f:
        f.write("# Archivo de prueba\n\n")
        f.write("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.0E03\n")
        f.write("2026-09-08 09:14:02 ADS3202 CH1 RUIDO 1.0E03\n")
    series, rechazos = leer_log(ruta_test)
    os.remove(ruta_test)
    
    assert len(rechazos) == 1
    assert rechazos[0]["linea"] == 4
    assert rechazos[0]["motivo"] == "la de magnitud que no es FREQ, PKPK ni CYCRMS"
    assert ("ADS3202", "CH1", "FREQ") in series
    assert series[("ADS3202", "CH1", "FREQ")][0] == 1000.0
    print("pruebas OK")
