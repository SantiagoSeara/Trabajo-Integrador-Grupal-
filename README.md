# Trabajo Final Integrador – Programación
## Un banco de mediciones automatizado en Python

Tecnicatura Universitaria en Telecomunicaciones – UTN FRBA · Ciclo lectivo 2026
Profesor a cargo: Pablo E. Hernández · Profesora ayudante: Candela Fernández Ibáñez

## Integrantes

- Jorge Santiago Tolaba
- Santiago Agustín Seara
- 

## Descripción

Programa en Python (solo biblioteca estándar) que se conecta por TCP a un osciloscopio virtual ADS3202, le pide mediciones con comandos SCPI, verifica que el Vrms medido coincida con el teórico de una senoidal (tolerancia 2 %), lee el registro histórico `mediciones.log` descartando las líneas inválidas, calcula estadísticas y escribe un informe.
Así mismo, a través de iteraciones, se corrobora y se genera un nuevo registro de mediciones, con el fin de corroborar y mantener un histórico de las nuevas mediciones. (El archivo Mediciones_nuevas_2.log es el primer archivo que se generó, pero el Mediciones_nuevas.log es el que funciona actualmente en caso de correr el código)

## Contenido del repositorio

| Archivo | Ejercicio |
| :--- | :--- |
| `01_identificacion.py` | Parseo de `*IDN?` |
| `02_magnitudes.py` | Conversión de números y prefijos (kHz, mV…) |
| `03_comandos.py` | Órdenes y consultas SCPI |
| `04_configurar.py` | Configuración de un canal |
| `05_cliente.py` | Cliente TCP (`Instrumento`) |
| `06_barrido.py` | Barrido de mediciones |
| `07_verificacion.py` | Verificación del Vrms |
| `08_log.py` | Lectura del registro de la sesión |
| `09_estadistica.py` | Estadística de una serie |
| `10_informe.py` | Informe final |
| `instrumento_virtual.py`, `mediciones.log` | Provistos por la cátedra, sin modificar |
| `mediciones_nuevas.log` | Historial acumulado de informes generados por el sistema |
| `bitacora-ia.md` | Bitácora de uso de IA |

## Archivos de pruebas

| Archivo | Descripción |
| :--- | :--- |
| `Mediciones_nuevas_2.log` | Iteración para conservar nuevos resultados |
| `Mediciones_nuevas.log` | Registro actual donde quedan grabadas las nuevas mediciones |

## Cómo ejecutarlo

Cada archivo corre solo y termina con `pruebas OK`:

```bash
python3 01_identificacion.py
```

Los ejercicios 5, 6 y 10 necesitan el instrumento virtual corriendo en otra terminal:

```bash
# Terminal 1
python3 instrumento_virtual.py

# Terminal 2
python3 05_cliente.py
python3 10_informe.py
```

El instrumento se apaga con `Ctrl+C`.
