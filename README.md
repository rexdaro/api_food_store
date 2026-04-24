# Proyecto Programación - Backend

API backend con Python, SQLModel y PostgreSQL.

## Requisitos previos

Antes de empezar, asegurate de tener instalado:

- **Python 3.12+** → [Descargar acá](https://www.python.org/downloads/)
- **PostgreSQL** → [Descargar acá](https://www.postgresql.org/download/)

## Paso a paso para correr el proyecto

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd proyecto_programacion
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
```

Activar el entorno virtual:

- **Windows (PowerShell):**
  ```bash
  .\venv\Scripts\Activate
  ```
- **Windows (CMD):**
  ```bash
  venv\Scripts\activate.bat
  ```
- **Linux / Mac:**
  ```bash
  source venv/bin/activate
  ```

> Vas a saber que está activo porque en la terminal aparece `(venv)` al inicio de la línea.

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos en PostgreSQL

Abrí **pgAdmin** o una terminal con `psql` y ejecutá:

```sql
CREATE DATABASE proyecto_programacion;
```

> **Nota:** Por defecto el proyecto se conecta con el usuario `postgres` y contraseña `803311` en `localhost:5432`. Si tu configuración es diferente, modificá el archivo `database.py` con tus datos.

### 5. Crear las tablas

```bash
python main.py
```

Esto crea automáticamente todas las tablas definidas en la carpeta `models/`.

Si todo sale bien, vas a ver: `Todo listo 🚀`

## Estructura del proyecto

```
proyecto_programacion/
├── main.py              # Punto de entrada - crea las tablas
├── database.py          # Configuración de conexión a PostgreSQL
├── models/
│   └── producto.py      # Modelo de la tabla "producto"
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Este archivo
```

## Solución de problemas

| Problema | Solución |
|---|---|
| `Cannot find module sqlmodel` | Asegurate de haber activado el entorno virtual y corrido `pip install -r requirements.txt` |
| Error de conexión a PostgreSQL | Verificá que PostgreSQL esté corriendo y que los datos en `database.py` sean correctos |
| `database "proyecto_programacion" does not exist` | Seguí el paso 4 para crear la base de datos |
