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
    parsear_idn = importlib.import_module("01_identificacion").parsear_idn
    try:
        osciloscopio = Instrumento()
    except ConnectionRefusedError:
        print("Fallo de conexión: corré 'python3 instrumento_virtual.py' en otra terminal.")
    else:
        respuesta_cruda = osciloscopio.preguntar("*IDN?")
        assert respuesta_cruda == "OWON,ADS3202,25470803,V1.2.0"

        datos_equipo = parsear_idn(respuesta_cruda)
        assert datos_equipo is not None
        assert datos_equipo["modelo"] == "ADS3202"

        osciloscopio.enviar(":CH2:DISPlay ON")
        assert osciloscopio.preguntar(":CH2:DISPlay?") == "ON"

        assert osciloscopio.preguntar(":NOEXISTE?") == "ERROR: comando desconocido"

        osciloscopio.cerrar()

        multimetro = Instrumento(puerto=5556)
        assert parsear_idn(multimetro.preguntar("*IDN?"))["modelo"] == "XDM1041"
        multimetro.cerrar()
        print("pruebas OK")
