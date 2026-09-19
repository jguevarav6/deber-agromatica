# Práctica 1 — Agromática y Bioinformática

Proyecto de Javier Guevara y Justin Minuche para almacenar y analizar datos
agrícolas y genéticos con PostgreSQL y Python.

## Requisitos

- Python 3.10 o superior.
- PostgreSQL y pgAdmin 4.
- Dependencias de `requirements.txt`.

## Instalación y ejecución

1. Crear y activar un entorno virtual.
2. Ejecutar `pip install -r requirements.txt`.
3. Abrir el Query Tool de pgAdmin conectado a `postgres` y ejecutar una sola
   vez `sql/01_crear_base.sql`.
4. Conectarse a `agrobio_db` y ejecutar `sql/02_esquema_datos.sql`.
5. Definir `AGRO_DB_PASSWORD` si el servidor exige contraseña. Las demás
   variables opcionales son `AGRO_DB_HOST`, `AGRO_DB_PORT`, `AGRO_DB_USER` y
   `AGRO_DB_NAME`.
6. Desde la raíz del proyecto, ejecutar `python -m src.agromatica`.
7. Ejecutar las pruebas con `pytest -v`.

Los gráficos se guardan en `salida/`.

La ejecución también guarda `salida/ejecucion_real.log`; pytest genera
`salida/pruebas_reales.log` mediante el hook incluido en `tests/conftest.py`.
