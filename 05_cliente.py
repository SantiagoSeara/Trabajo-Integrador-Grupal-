import socket
from 01_identificacion import parsear_idn

class Instrumento:
    def __init__(self, direccion="127.0.0.1", puerto=5555):
        # socket.AF_INET indica IPv4, socket.SOCK_STREAM indica TCP
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexion.connect((direccion, puerto))

    def enviar(self, comando):
        """Manda una orden y no espera nada (ENVIAR)"""
        # Se asegura de agregar el salto de línea obligatorio
        mensaje = f"{comando}\n"
        self.conexion.sendall(mensaje.encode('utf-8'))

    def preguntar(self, comando):
        """Manda una consulta y devuelve la respuesta (QUERY)"""
        # Reutilizamos el método enviar para no repetir lógica
        self.enviar(comando)
        
        # Leemos la respuesta, la decodificamos y le quitamos el salto de línea final
        respuesta = self.conexion.recv(1024).decode('utf-8')
        return respuesta.strip('\n')

    def cerrar(self):
        """Cierra la conexión TCP"""
        self.conexion.close()

# ==========================================
# BLOQUE DE PRUEBAS (asserts)
# ==========================================

# Esta validación evita que el archivo se ejecute si es importado desde otro lado,
# pero corre las pruebas si lo ejecutás directamente en la terminal.
if __name__ == '__main__':
    try:
        # Valores por defecto: 127.0.0.1 y 5555 (osciloscopio)
        osciloscopio = Instrumento()
        
        # Prueba mínima de la cátedra[cite: 10]
        respuesta_cruda = osciloscopio.preguntar("*IDN?")
        assert respuesta_cruda == "OWON, ADS3202,25470803, V1.2.0"
        
        # Validación con la función del ejercicio 1[cite: 10]
        datos_equipo = parsear_idn(respuesta_cruda)
        assert datos_equipo is not None
        assert datos_equipo["modelo"] == "ADS3202"
        
        osciloscopio.cerrar()
        print("pruebas OK")
        
    except ConnectionRefusedError:
        print("Fallo de conexión: Asegurate de correr 'python3 instrumento_virtual.py' en otra terminal antes de probar este archivo.")