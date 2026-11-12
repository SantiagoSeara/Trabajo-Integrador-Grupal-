import importlib

"""Módulo de generación del informe de mediciones.

Este archivo reúne la identificación del instrumento, los valores históricos
medidos y la verificación del barrido actual para producir un texto legible
que puede mostrarse por consola o guardarse en archivo.
"""


def armar_informe(idn, series, verificaciones):
    """Construye un resumen textual a partir de los datos del instrumento.

    Acotación:
    La función centraliza la presentación: no decide cómo medir, sino cómo
    comunicar los resultados para que el usuario pueda interpretarlos fácilmente.
    """
    con_unidad = importlib.import_module("02_magnitudes").con_unidad
    resumen = importlib.import_module("09_estadistica").resumen

    lineas = []
    lineas.append("=== INFORME DE MEDICIONES ===")
    if idn:
        lineas.append(f"Instrumento: {idn['fabricante']} {idn['modelo']} (Serie: {idn['serie']} - v{idn['version']})")
    else:
        lineas.append("Instrumento: Desconocido")

    # Sección 1: resumen de la historia registrada. Aquí se muestran las
    # series con sus estadísticos básicos, útiles para comparar tendencias y
    # detectar anomalías de forma rápida.
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

    # Sección 2: comparación entre la medición actual y el valor teórico.
    # Esto permite validar si el canal está dentro de la tolerancia esperada.
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
    # Bloque de validación rápida: sirve para comprobar que el formato del
    # informe sea consistente antes de intentar usarlo con equipo real.
    idn_test = {"fabricante": "OWON", "modelo": "ADS3202", "serie": "123", "version": "V1.0"}
    series_test = {("ADS3202", "CH1", "FREQ"): [1000.0, 1005.0]}
    verif_test = [{"canal": "CH1", "vrms_medido": 0.71, "vrms_teorico": 0.707, "coincide": True}]
    texto_informe = armar_informe(idn_test, series_test, verif_test)
    assert "OWON ADS3202" in texto_informe
    assert "Promedio 1.002 kHz" in texto_informe
    assert "CH1: PASA" in texto_informe
    print("pruebas OK")

    try:
        # Acotación: este bloque se ejecuta solo cuando el instrumento está
        # disponible y puede responder a una consulta de identificación.
        Instrumento = importlib.import_module("05_cliente").Instrumento
        parsear_idn = importlib.import_module("01_identificacion").parsear_idn
        barrer = importlib.import_module("06_barrido").barrer
        verificar_canal = importlib.import_module("07_verificacion").verificar_canal
        leer_log = importlib.import_module("08_log").leer_log

        osciloscopio = Instrumento()
        respuesta_idn = osciloscopio.preguntar("*IDN?")
        idn_datos = parsear_idn(respuesta_idn)

        # Se realiza el barrido de los canales para obtener los valores actuales
        # que luego serán comparados con la referencia teórica o histórica.
        mediciones_actuales = barrer(osciloscopio, ["CH1", "CH2"])
        osciloscopio.cerrar()

        verificaciones_actuales = [
            verificar_canal(mediciones_actuales, "CH1"),
            verificar_canal(mediciones_actuales, "CH2")
        ]

        # Se lee el archivo de log histórico para incorporar las series previas
        # dentro del mismo informe generado para el usuario.
        series_hist, rechazos = leer_log("mediciones.log")
        informe_final = armar_informe(idn_datos, series_hist, verificaciones_actuales)

        # En la práctica, esta línea se repite para dejar evidencia del mismo
        # proceso de lectura, pero el informe final se construye a partir de la
        # versión cargada en memoria más reciente.
        # series_hist, rechazos = leer_log("mediciones.log")
        # informe_final = armar_informe(idn_datos, series_hist, verificaciones_actuales)

        # Guarda una copia resumida del comportamiento histórico en un archivo
        # auxiliar para su revisión posterior.
        import datetime
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        con_unidad = importlib.import_module("02_magnitudes").con_unidad
        resumen = importlib.import_module("09_estadistica").resumen

        with open("mediciones_nuevas.log", "a", encoding="utf-8") as log_nuevo:
            log_nuevo.write(f"--- Ejecución: {ahora} ---\n")

            for clave, valores in series_hist.items():
                equipo, canal, magnitud = clave
                datos = resumen(valores)
                if datos:
                    unidad = "Hz" if magnitud == "FREQ" else "V"
                    prom = con_unidad(datos['promedio'], unidad)
                    minimo = con_unidad(datos['minimo'], unidad)
                    maximo = con_unidad(datos['maximo'], unidad)

                    linea = f"{equipo} {canal} {magnitud} (n={datos['n']}): Promedio {prom} | Min {minimo} | Max {maximo}\n"
                    log_nuevo.write(linea)
            log_nuevo.write("\n")

        # Muestra el texto final por consola para que el usuario vea el resultado
        # del análisis completo en forma legible.
        print("\n" + informe_final)

    except ConnectionRefusedError:
        print("Para ver el informe final, ejecutar instrumento_virtual.py en otra terminal.")
    except FileNotFoundError:
        print("No se encontró mediciones.log. Asegurate de tenerlo en la misma carpeta.")
log. Asegurate de tenerlo en la misma carpeta.")
