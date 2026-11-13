"""Ejercicio 10: arma el informe del banco de mediciones."""
import importlib

con_unidad = importlib.import_module("02_magnitudes").con_unidad
resumen = importlib.import_module("09_estadistica").resumen


def armar_informe(idn, series, verificaciones):
    lineas = []
    lineas.append("=== INFORME DE MEDICIONES ===")
    if idn:
        lineas.append(f"Instrumento: {idn['fabricante']} {idn['modelo']} (Serie: {idn['serie']} - {idn['version']})")
    else:
        lineas.append("Instrumento: Desconocido")

    lineas.append("")
    lineas.append("--- SERIES DEL LOG ---")
    for clave, valores in series.items():
        equipo, canal, magnitud = clave
        datos = resumen(valores)
        if datos:
            unidad = "Hz" if magnitud == "FREQ" else "V"
            prom_str = con_unidad(datos['promedio'], unidad)
            min_str = con_unidad(datos['minimo'], unidad)
            max_str = con_unidad(datos['maximo'], unidad)
            lineas.append(f"{equipo} {canal} {magnitud} (n={datos['n']}): Promedio {prom_str} | Min {min_str} | Max {max_str}")

    lineas.append("")
    lineas.append("--- VERIFICACIÓN DEL BARRIDO ACTUAL ---")
    for verif in verificaciones:
        canal = verif["canal"]
        if verif['vrms_medido'] is not None and verif['vrms_teorico'] is not None:
            estado = "PASA" if verif["coincide"] else "FALLA"
            medido = con_unidad(verif['vrms_medido'], "V")
            teorico = con_unidad(verif['vrms_teorico'], "V")
            lineas.append(f"{canal}: {estado} (Vrms medido: {medido} | Vrms teórico: {teorico})")
        else:
            lineas.append(f"{canal}: FALLA (faltan datos para verificar)")

    return "\n".join(lineas)


if __name__ == '__main__':
    idn_test = {"fabricante": "OWON", "modelo": "ADS3202", "serie": "123", "version": "V1.0"}
    series_test = {("ADS3202", "CH1", "FREQ"): [1000.0, 1005.0]}
    verif_test = [
        {"canal": "CH1", "vrms_medido": 0.71, "vrms_teorico": 0.707, "coincide": True},
        {"canal": "CH2", "vrms_medido": 1.0, "vrms_teorico": 0.707, "coincide": False},
        {"canal": "CH3", "vrms_medido": None, "vrms_teorico": None, "coincide": False}
    ]
    texto = armar_informe(idn_test, series_test, verif_test)
    assert isinstance(texto, str)
    assert texto.split("\n")[0] == "=== INFORME DE MEDICIONES ==="
    assert "--- SERIES DEL LOG ---" in texto
    assert "--- VERIFICACIÓN DEL BARRIDO ACTUAL ---" in texto
    assert "OWON ADS3202" in texto
    assert "ADS3202 CH1 FREQ (n=2): Promedio 1.002 kHz | Min 1 kHz | Max 1.005 kHz" in texto
    assert "CH1: PASA" in texto
    assert "CH2: FALLA" in texto
    assert "CH3: FALLA (faltan datos" in texto
    assert "Instrumento: Desconocido" in armar_informe(None, {}, [])
    print("pruebas OK")

    Instrumento = importlib.import_module("05_cliente").Instrumento
    parsear_idn = importlib.import_module("01_identificacion").parsear_idn
    barrer = importlib.import_module("06_barrido").barrer
    verificar_canal = importlib.import_module("07_verificacion").verificar_canal
    leer_log = importlib.import_module("08_log").leer_log

    try:
        osciloscopio = Instrumento()
    except ConnectionRefusedError:
        print("Para ver el informe final, ejecutar instrumento_virtual.py en otra terminal.")
    else:
        idn_datos = parsear_idn(osciloscopio.preguntar("*IDN?"))
        mediciones = barrer(osciloscopio, ["CH1", "CH2"])
        osciloscopio.cerrar()

        verificaciones = [verificar_canal(mediciones, canal) for canal in ("CH1", "CH2")]
        series, rechazos = leer_log("mediciones.log")

        print()
        print(armar_informe(idn_datos, series, verificaciones))
        print()
        print(f"Líneas rechazadas del log: {len(rechazos)}")
        for r in rechazos:
            print(f"  línea {r['linea']}: {r['motivo']} -> {r['texto']}")
