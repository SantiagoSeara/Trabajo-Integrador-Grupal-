import datetime
import importlib
import math

"""Módulo de generación del informe de mediciones."""


def _es_numero_valido(valor):
    """Devuelve True si valor es un número real finito (ni None ni NaN)."""
    if valor is None:
        return False
    try:
        v = float(valor)
        return not math.isnan(v) and not math.isinf(v)
    except (ValueError, TypeError):
        return False


def _integrar_barrido_a_series(series_hist, idn_datos, mediciones_actuales):
    """Agrega la lista de 6 diccionarios de 06_barrido.py a series_hist."""
    equipo = idn_datos["modelo"] if idn_datos and "modelo" in idn_datos else "ADS3202"

    for item in mediciones_actuales:
        valor = item.get("valor_convertido")
        if _es_numero_valido(valor):
            clave = (equipo, item["canal"], item["magnitud"])
            series_hist.setdefault(clave, []).append(float(valor))


def armar_informe(idn, series, verificaciones, mediciones_actuales=None, rechazos=None):
    """Construye un resumen textual a partir de los datos del instrumento."""
    con_unidad = importlib.import_module("02_magnitudes").con_unidad
    resumen = importlib.import_module("09_estadistica").resumen

    lineas = []
    lineas.append("=== INFORME DE MEDICIONES ===")
    if idn:
        lineas.append(
            f"Instrumento: {idn['fabricante']} {idn['modelo']} "
            f"(Serie: {idn['serie']} | Firmware: {idn['version']})"
        )
    else:
        lineas.append("Instrumento: Desconocido")

    # Sección 1: detalle de las 6 mediciones del barrido actual
    if mediciones_actuales:
        lineas.append("\n--- MEDICIONES DEL BARRIDO ACTUAL ---")
        for item in mediciones_actuales:
            canal = item["canal"]
            magnitud = item["magnitud"]
            unidad = item["unidad"]
            valor = item["valor_convertido"]
            if _es_numero_valido(valor):
                lineas.append(f"{canal} {magnitud}: {con_unidad(valor, unidad)}")
            else:
                lineas.append(f"{canal} {magnitud}: ERROR ({item['texto_crudo']})")

    # Sección 2: resumen de la historia registrada (sin NaN)
    lineas.append("\n--- SERIES HISTÓRICAS ---")
    if not series:
        lineas.append("Sin series históricas registradas.")
    else:
        for clave, valores in series.items():
            equipo, canal, magnitud = clave
            valores_limpios = [float(v) for v in valores if _es_numero_valido(v)]
            datos = resumen(valores_limpios)
            if datos:
                unidad = "Hz" if magnitud == "FREQ" else "V"
                prom_str = con_unidad(datos['promedio'], unidad)
                min_str = con_unidad(datos['minimo'], unidad)
                max_str = con_unidad(datos['maximo'], unidad)
                lineas.append(
                    f"{equipo} {canal} {magnitud} (n={datos['n']}): "
                    f"Promedio {prom_str} | Min {min_str} | Max {max_str}"
                )

    # Sección 3: comparación entre la medición actual y el valor teórico
    lineas.append("\n--- VERIFICACIÓN DEL BARRIDO ACTUAL ---")
    for verif in verificaciones:
        canal = verif["canal"]
        estado = "PASA" if verif["coincide"] else "FALLA"
        if verif['vrms_medido'] is not None and verif['vrms_teorico'] is not None:
            lineas.append(
                f"{canal}: {estado} (Medido: {round(verif['vrms_medido'], 4)} V | "
                f"Teórico: {round(verif['vrms_teorico'], 4)} V)"
            )
        else:
            lineas.append(f"{canal}: FALLA (Faltan datos para verificar)")

    # Sección 4: líneas descartadas/corruptas del log (solo si se pasan)
    if rechazos:
        lineas.append(f"\n--- REGISTROS RECHAZADOS DEL LOG ({len(rechazos)}) ---")
        for r in rechazos:
            lineas.append(f"  - {r}")

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
        _integrar_barrido_a_series(series_hist, idn_datos, mediciones_actuales)

        # Informe para guardar en mediciones_nuevas.log (sin rechazos)
        informe_log = armar_informe(
            idn_datos,
            series_hist,
            verificaciones_actuales,
            mediciones_actuales=mediciones_actuales,
            rechazos=None
        )

        # Informe para mostrar por consola (con rechazos)
        informe_consola = armar_informe(
            idn_datos,
            series_hist,
            verificaciones_actuales,
            mediciones_actuales=mediciones_actuales,
            rechazos=rechazos
        )

        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("mediciones_nuevas.log", "a", encoding="utf-8") as log_nuevo:
            log_nuevo.write(f"--- Ejecución: {ahora} ---\n")
            log_nuevo.write(informe_log + "\n\n")

        print("\n" + informe_consola)

    except ConnectionRefusedError:
        print("Para ver el informe final, ejecutar instrumento_virtual.py en otra terminal.")
    except FileNotFoundError:
        print("No se encontró mediciones.log. Asegurate de tenerlo en la misma carpeta.")
        print("Para ver el informe final, ejecutar instrumento_virtual.py en otra terminal.")
    except FileNotFoundError:
        print("No se encontró mediciones.log. Asegurate de tenerlo en la misma carpeta.")

