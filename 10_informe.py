from 02_magnitudes import con_unidad
from 09_estadistica import resumen

def armar_informe(idn, series, verificaciones):
    """Genera el informe completo como texto puro."""
    # EVIDENCIA: La función no debe imprimir nada ni abrir archivos, solo devuelve texto[cite: 13].
    lineas = []
    
    # 1. Identificación del instrumento
    lineas.append("=== INFORME DE MEDICIONES ===")
    if idn:
        lineas.append(f"Instrumento: {idn['fabricante']} {idn['modelo']} (Serie: {idn['serie']} - v{idn['version']})")
    else:
        lineas.append("Instrumento: Desconocido")
        
    lineas.append("\n--- SERIES HISTÓRICAS ---")
    
    # 2. Resumen de las series
    # DIAGNÓSTICO: Recorremos el diccionario de series agrupadas por equipo, canal y magnitud.
    for clave, valores in series.items():
        equipo, canal, magnitud = clave
        datos = resumen(valores)
        
        if datos:
            # Determinamos la unidad base según la magnitud (Hz para FREQ, V para el resto)
            unidad = "Hz" if magnitud == "FREQ" else "V"
            
            # COMPROBÉ: Usamos con_unidad() para mostrar números legibles como pide la consigna[cite: 13].
            prom_str = con_unidad(datos['promedio'], unidad)
            min_str = con_unidad(datos['minimo'], unidad)
            max_str = con_unidad(datos['maximo'], unidad)
            
            lineas.append(f"{equipo} {canal} {magnitud} (n={datos['n']}): Promedio {prom_str} | Min {min_str} | Max {max_str}")
    
    lineas.append("\n--- VERIFICACIÓN DEL BARRIDO ACTUAL ---")
    
    # 3. Resultado de verificaciones
    for verif in verificaciones:
        canal = verif["canal"]
        estado = "PASA" if verif["coincide"] else "FALLA"
        
        if verif['vrms_medido'] is not None and verif['vrms_teorico'] is not None:
            lineas.append(f"{canal}: {estado} (Medido: {round(verif['vrms_medido'], 4)} V | Teórico: {round(verif['vrms_teorico'], 4)} V)")
        else:
            lineas.append(f"{canal}: FALLA (Faltan datos para verificar)")
            
    # Unimos todas las líneas con saltos de línea (\n)
    return "\n".join(lineas)

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# PREDIGO: Le paso diccionarios y listas de prueba, y la función tiene que devolver 
# el texto correctamente ensamblado y con las unidades convertidas.
idn_test = {"fabricante": "OWON", "modelo": "ADS3202", "serie": "123", "version": "V1.0"}
series_test = {("ADS3202", "CH1", "FREQ"): [1000.0, 1005.0]}
verif_test = [{"canal": "CH1", "vrms_medido": 0.71, "vrms_teorico": 0.707, "coincide": True}]

texto_informe = armar_informe(idn_test, series_test, verif_test)

# Evaluamos que las piezas clave estén dentro de la cadena final
assert "OWON ADS3202" in texto_informe
assert "Promedio 1 kHz" in texto_informe  # Chequea que llamó bien a con_unidad()
assert "CH1: PASA" in texto_informe

print("pruebas OK")

# ==========================================
# EJECUCIÓN DEL PROGRAMA COMPLETO[cite: 14]
# ==========================================
if __name__ == '__main__':
    try:
        # CREO: Importamos el resto de las piezas solo cuando se ejecuta este archivo 
        # como principal, evitando dependencias circulares durante los tests.
        from 05_cliente import Instrumento
        from 01_identificacion import parsear_idn
        from 06_barrido import barrer
        from 07_verificacion import verificar_canal
        from 08_log import leer_log
        
        # 1. Identificar equipo[cite: 14]
        osciloscopio = Instrumento()
        respuesta_idn = osciloscopio.preguntar("*IDN?")
        idn_datos = parsear_idn(respuesta_idn)
        
        # 2. Barrer canales[cite: 14]
        mediciones_actuales = barrer(osciloscopio, ["CH1", "CH2"])
        osciloscopio.cerrar()
        
        # 3. Verificarlos[cite: 14]
        verificaciones_actuales = [
            verificar_canal(mediciones_actuales, "CH1"),
            verificar_canal(mediciones_actuales, "CH2")
        ]
        
        # 4. Leer log[cite: 14]
        # ENCONTRÉ: Requiere que mediciones.log entregado por la cátedra esté en la misma carpeta.
        series_hist, rechazos = leer_log("mediciones.log")
        
        # 5. Escribir informe en pantalla[cite: 14]
        informe_final = armar_informe(idn_datos, series_hist, verificaciones_actuales)
        print("\n" + informe_final)
        
    except ConnectionRefusedError:
        print("Para ver el informe final, recordá ejecutar 'python3 instrumento_virtual.py' en otra terminal.")
    except FileNotFoundError:
        print("No se encontró mediciones.log. Asegurate de tenerlo en la misma carpeta.")