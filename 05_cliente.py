import socket
import importlib

class Instrumento:
    def __init__(self, direccion="127.0.0.1", puerto=5555):
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexion.connect((direccion, puerto))

    def enviar(self, comando):
        mensaje = f"{comando}\n"
        self.conexion.sendall(mensaje.encode('utf-8'))

    def preguntar(self, comando):
        self.enviar(comando)
        respuesta = self.conexion.recv(1024).decode('utf-8')
        return respuesta.strip('\n')

    def cerrar(self):
        self.conexion.close()

if __name__ == '__main__':
    try:
        parsear_idn = importlib.import_module("01_identificacion").parsear_idn
        osciloscopio = Instrumento()
        respuesta_cruda = osciloscopio.preguntar("*IDN?")
        assert respuesta_cruda == "OWON, ADS3202,25470803, V1.2.0"
        
        datos_equipo = parsear_idn(respuesta_cruda)
        assert datos_equipo is not None
        assert datos_equipo["modelo"] == "ADS3202"
        
        osciloscopio.cerrar()
        print("pruebas OK")
    except ConnectionRefusedError:
        print("Fallo de conexión: Prender instrumento_virtual.py")
onRefusedError:
        print("Fallo de conexión: Asegurate de correr 'python3 instrumento_virtual.py' en otra terminal antes de probar este archivo.")
