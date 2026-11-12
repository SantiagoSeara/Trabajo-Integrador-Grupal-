# Importamos la función del ejercicio 3 exclusivamente para las pruebas
from 03_comandos import validar

def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    """Devuelve la lista de 4 comandos de configuración. Si el canal no existe, devuelve None."""
    if canal not in ("CH1", "CH2"):
        return None
        
    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}"
    ]

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Prueba 1: Comprobación exacta de la lista de salida esperada[cite: 9, 10]
esperado = [
    ":CH1:DISPlay ON",
    ":CH1:COUPling DC",
    ":CH1:PROBe 10X",
    ":CH1:SCALe 1v"
]
assert comandos_de_canal("CH1", "ON", "DC", "10X", "1v") == esperado

# Prueba 2: Caso raro - Canal inválido[cite: 7, 9]
assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None

# Prueba 3: LA PRUEBA QUE VALE POR DIEZ[cite: 10]
# Verificamos que los 4 comandos generados pasen la validación estricta del Ejercicio 3
comandos = comandos_de_canal("CH2", "OFF", "AC", "1X", "500mv")
for cmd in comandos:
    assert validar(cmd) is None, f"El comando {cmd} falló la validación"

print("pruebas OK")