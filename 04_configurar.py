import importlib

def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    if canal not in ("CH1", "CH2"):
        return None
    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}"
    ]

if __name__ == '__main__':
    validar = importlib.import_module("03_comandos").validar
    
    esperado = [
        ":CH1:DISPlay ON",
        ":CH1:COUPling DC",
        ":CH1:PROBe 10X",
        ":CH1:SCALe 1v"
    ]
    assert comandos_de_canal("CH1", "ON", "DC", "10X", "1v") == esperado
    assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
    
    comandos = comandos_de_canal("CH2", "OFF", "AC", "1X", "500mv")
    for cmd in comandos:
        assert validar(cmd) is None, f"El comando {cmd} falló la validación"
    print("pruebas OK")
print("pruebas OK")
