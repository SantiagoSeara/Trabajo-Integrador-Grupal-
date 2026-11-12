import os
from 02_magnitudes import a_numero

def analizar_linea(linea):
    """Evalúa una línea del log. Devuelve (medición, None) si es válida, 
    (None, motivo) si se rechaza, y (None, None) si se ignora."""
    # Limpiamos espacios en blanco o saltos de línea en los extremos
    linea_limpia = linea.strip()
    
    # 1. IGNORAR: línea en blanco o comentario con #[cite: 12]
    if not linea_limpia or linea_limpia.startswith('#'):
        return (None, None)
        
    # 2. SEPARAR: split() sin argumentos es la clave para la trampa de las tabulaciones
    campos = linea_limpia.split()
    
    # 3. RECHAZAR: Validaciones secuenciales[cite: 12]
    if len(campos) != 6:
        return (None, "la que no tiene exactamente seis campos")
        
    # Extraemos y validamos la hora (HH:MM:SS) usando los métodos de cadena y conversión
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
        
    # Si pasó todos los filtros, armamos el diccionario de la medición
    medicion = {
        "fecha": campos[0],
        "hora": campos[1],
        "equipo": campos[2],
        "canal": campos[3],
        "magnitud": campos[4],
        "valor": valor
    }
    
    return (medicion, None)

def leer_log(ruta):
    """Recorre el archivo y devuelve las series agrupadas y la lista de rechazos."""
    series = {}
    rechazos = []
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        # enumerate nos da el número de línea automáticamente
        for num, linea in enumerate(archivo, 1):
            medicion, motivo = analizar_linea(linea)
            
            # Línea ignorada (ej. en blanco) -> pasamos a la siguiente
            if medicion is None and motivo is None:
                continue
                
            # Línea rechazada -> guardamos el motivo y el número[cite: 12]
            if motivo is not None:
                rechazos.append({"linea": num, "motivo": motivo})
            else:
                # Línea válida -> Agrupamos usando una tupla (equipo, canal, magnitud)[cite: 12]
                clave = (medicion["equipo"], medicion["canal"], medicion["magnitud"])
                if clave not in series:
                    series[clave] = []
                series[clave].append(medicion["valor"])
                
    return series, rechazos

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Pruebas de analizar_linea()
# Caso de ignorar[cite: 12]
assert analizar_linea("") == (None, None)
assert analizar_linea("# Inicio de mediciones") == (None, None)

# Casos de rechazo[cite: 12]
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ")[1] == "la que no tiene exactamente seis campos"
assert analizar_linea("2026-09-08 25:61:00 ADS3202 CH1 FREQ 1E03")[1] == "la de hora imposible"
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH3 FREQ 1E03")[1] == "la de canal que no es CH1 ni CH2"
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 RUIDO 1E03")[1] == "la de magnitud que no es FREQ, PKPK ni CYCRMS"
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ ERROR")[1] == "la de valor que no se puede convertir a número"

# Caso de éxito con la trampa de tabulaciones (campos separados por \t en lugar de espacio)[cite: 13]
linea_tabulada = "2026-09-08\t09:14:02\tADS3202\tCH1\tFREQ\t1.000431E+03"
medicion_ok, motivo = analizar_linea(linea_tabulada)
assert motivo is None
assert medicion_ok["valor"] == 1000.431

# Prueba integradora de leer_log() generando un archivo temporal
ruta_test = "test_temp.log"
with open(ruta_test, "w") as f:
    f.write("# Archivo de prueba\n")
    f.write("\n")
    f.write("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.0E03\n")
    f.write("2026-09-08 09:14:02 ADS3202 CH1 RUIDO 1.0E03\n") # Para que salte un rechazo

series, rechazos = leer_log(ruta_test)

# Limpiamos el archivo de prueba
os.remove(ruta_test)

# Verificamos que procesó correctamente
assert len(rechazos) == 1
assert rechazos[0]["linea"] == 4
assert rechazos[0]["motivo"] == "la de magnitud que no es FREQ, PKPK ni CYCRMS"
assert ("ADS3202", "CH1", "FREQ") in series
assert series[("ADS3202", "CH1", "FREQ")][0] == 1000.0

print("pruebas OK")