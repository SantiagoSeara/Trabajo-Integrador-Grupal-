# Trabajo Final Integrador – Programación
## Un banco de mediciones automatizado en Python

Tecnicatura Universitaria en Telecomunicaciones – UTN FRBA · Ciclo lectivo 2026
Profesor a cargo: Pablo E. Hernández · Profesora ayudante: Candela Fernández Ibáñez

## Integrantes

. Jorge Santiago Tolaba
. 
. 
. 
. 

## Descripción

Programa en Python (solo biblioteca estándar) que se conecta por TCP a un osciloscopio virtual ADS3202, le pide mediciones con comandos SCPI, verifica que el Vrms medido coincida con el teórico de una senoidal (tolerancia 2 %), lee el registro histórico `mediciones.log` descartando las líneas inválidas, calcula estadísticas y escribe un informe.

## Contenido del repositorio

| Archivo | Ejercicio |
|---|---|
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
| `bitacora-ia.md` | Bitácora de uso de IA |

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
