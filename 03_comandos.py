def es_consulta(comando):
    """Devuelve True si el comando termina en ?"""
    if not comando:
        return False
    return comando.endswith('?')

def validar(comando):
    """Devuelve None si el comando es válido, o un mensaje de error si rompe alguna regla."""
    if not comando:
        return "No puede estar vacío"
        
    if not (comando.startswith(':') or comando.startswith('*')):
        return "Empieza con : o con *"
        
    if "  " in comando:
        return "No hay dos espacios seguidos"
        
    if comando.count('?') > 1:
        return "Hay a lo sumo un ?"
        
    if '?' in comando and not comando.endswith('?'):
        return "El ? va al final"
        
    # Separar por espacio nos permite ver la cantidad de argumentos.
    partes = comando.split(" ")
    
    if es_consulta(comando):
        # Si es consulta, no debe tener espacios (len tiene que ser 1)
        if len(partes) > 1:
            return "Una consulta no lleva argumento"
    else:
        # Si es orden, tiene que tener un solo argumento (el comando y el argumento, len tiene que ser 2)
        if len(partes) != 2:
            return "Una orden lleva un solo argumento"
            
    return None

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Pruebas de es_consulta()
assert es_consulta(":CH1:DISPlay?") is True
assert es_consulta(":CH1:DISPlay ON") is False
assert es_consulta("") is False

# Pruebas de validar() con casos correctos
assert validar("*IDN?") is None
assert validar(":CH1:DISPlay ON") is None
assert validar(":MEASUrement:CH1:FREQuency?") is None

# Pruebas de validar() basadas en la tabla de la cátedra[cite: 9]
assert validar("") == "No puede estar vacío"
assert validar("CH1:DISPlay ON") == "Empieza con : o con *"
assert validar(":CH1:DISPlay  ON") == "No hay dos espacios seguidos"
assert validar(":CH1:DISPlay??") == "Hay a lo sumo un ?"
assert validar(":CH1:DIS?Play") == "El ? va al final"
assert validar(":CH1:SCALe 1 v") == "Una orden lleva un solo argumento"
assert validar(":CH1:DISPlay ON?") == "Una consulta no lleva argumento"

print("pruebas OK")