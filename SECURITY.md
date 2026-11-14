## Alcance del Proyecto

Este repositorio corresponde al **Trabajo Final Integrador (TFI)** de la materia **Programación** (*Tecnicatura Universitaria en Telecomunicaciones – UTN FRBA, Ciclo lectivo 2026*). El sistema implementa un cliente TCP para comunicación **SCPI** con instrumentación virtual (`OWON ADS3202`) y procesamiento de registros históricos.

## Versiones Soportadas

| Versión / Rama | Estado | Soporte |
| :--- | :--- | :--- |
| `main` (Entrega final 2026) | Activa | Soportada |
| Ramas de desarrollo / borradores | Obsoleta | Sin soporte |

## Consideraciones de Seguridad del Diseño

Dado que el sistema opera sobre sockets de red y archivos de texto externos, se aplican los siguientes controles defensivos en el código:

1. **Aislamiento de Red (`05_cliente.py`):** La conexión TCP se establece por defecto únicamente sobre la interfaz de bucle local (`127.0.0.1`, puerto `5555`), evitando exposición a interfaces externas sin configuración explícita.
2. **Validación Sintáctica de Comandos SCPI (`03_comandos.py`):** Toda instrucción pasa por reglas estrictas de formato (prefijo `:` o `*`, ausencia de espacios dobles, única marca `?` al final y control de argumentos) antes de su envío.
3. **Sanitización de Registros Externos (`08_log.py` y `10_informe.py`):** El analizador de `mediciones.log` descarta líneas malformadas, marcas temporales fuera de rango, canales no autorizados y valores no finitos (`NaN`, `Inf`) antes de procesar estadísticas.
4. **Cero Dependencias de Terceros:** El proyecto utiliza exclusivamente la biblioteca estándar de Python, eliminando riesgos de cadena de suministro (*supply chain*) asociados a paquetes externos.

## Reporte de Vulnerabilidades o Fallos

Al tratarse de un proyecto de uso estrictamente académico y laboratorio local:

* No almacena credenciales, tokens ni datos personales sensibles.
* No debe exponerse el simulador ni el cliente directamente a redes públicas sin cifrado o control de acceso.
* Ante cualquier comportamiento anómalo o fallo detectado en los módulos (`01` a `10`), reportarlo mediante un **Issue** en este repositorio o comunicarse con los autores del proyecto.
