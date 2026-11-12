import importlib

def armar_informe(idn, series, verificaciones):
    con_unidad = importlib.import_module("02_magnitudes").con_unidad
    resumen = importlib.import_module("09_estadistica").resumen
    
    lineas = []
    lineas.append("=== INFORME DE MEDICIONES ===")
    if idn:
        lineas.append(f"Instrumento: {idn['fabricante']} {idn['modelo']} (Serie: {idn['serie']} - v{idn['version']})")
    else:
        lineas.append("Instrumento: Desconocido")
        
    lineas.append("\n--- SERIES HISTÓRICAS ---")
    for clave, valores in series.items():
        equipo, canal, magnitud = clave
        datos = resumen(valores)
        if datos:
            unidad = "Hz" if magnitud == "FREQ" else "V"
            prom_str = con_unidad(datos['promedio'], unidad)
            min_str = con_unidad(datos['minimo'], unidad)
            max_str = con_unidad(datos['maximo'], unidad)
            lineas.append(f"{equipo} {canal} {magnitud} (n={datos['n']}): Promedio {prom_str} | Min {min_str} | Max {max_str}")
            
    lineas.append("\n--- VERIFICACIÓN DEL BARRIDO ACTUAL ---")
    for verif in verificaciones:
        canal = verif["canal"]
        estado = "PASA" if verif["coincide"] else "FALLA"
        if verif['vrms_medido'] is not None and verif['vrms_teorico'] is not None:
            lineas.append(f"{canal}: {estado} (Medido: {round(verif['vrms_medido'], 4)} V | Teórico: {round(verif['vrms_teorico'], 4)} V)")
        else:
            lineas.append(f"{canal}: FALLA (Faltan datos para verificar)")
            
    return "\n".join(lineas)

if __name__ == '__main__':
    idn_test = {"fabricante": "OWON", "modelo": "ADS3202", "serie": "123", "version": "V1.0"}
    series_test = {("ADS3202", "CH1", "FREQ"): [1000.0, 1005.0]}
    verif_test = [{"canal": "CH1", "vrms_medido": 0.71, "vrms_teorico": 0.707, "coincide": True}]
    texto_informe = armar_informe(idn_test, series_test, verif_test)
    assert "OWON ADS3202" in texto_informe
    assert "Promedio 1.002 kHz" in texto_informe
    assert "CH1: PASA" in texto_informe
    print("pruebas OK")

    try:
        Instrumento = importlib.import_module("05_cliente").Instrumento
        parsear_idn = importlib.import_module("01_identificacion").parsear_idn
        barrer = importlib.import_module("06_barrido").barrer
        verificar_canal = importlib.import_module("07_verificacion").verificar_canal
        leer_log = importlib.import_module("08_log").leer_log
        
        osciloscopio = Instrumento()
        respuesta_idn = osciloscopio.preguntar("*IDN?")
        idn_datos = parsear_idn(respuesta_idn)
        
        mediciones_actuales = barrer(osciloscopio, ["CH1", "CH2"])
        osciloscopio.cerrar()
        
        verificaciones_actuales = [
            verificar_canal(mediciones_actuales, "CH1"),
            verificar_canal(mediciones_actuales, "CH2")
        ]
        
        series_hist, rechazos = leer_log("mediciones.log")
        informe_final = armar_informe(idn_datos, series_hist, verificaciones_actuales)
        print("\n" + informe_final)
        
    except ConnectionRefusedError:
        print("Para ver el informe final, ejecutar instrumento_virtual.py en otra terminal.")
    except FileNotFoundError:
        print("No se encontró mediciones.log. Asegurate de tenerlo en la misma carpeta.")
