# ⚙️ FoodStore Backend API

API robusta construida con FastAPI y SQLModel para la gestión del sistema FoodStore.

## 🚀 Inicio Rápido

1. Crear venv: `python -m venv venv`
2. Activar venv y `pip install -r requirements.txt`
3. Ejecutar: `uvicorn app.main:app --reload`

## 📊 Base de Datos
- **Motor**: PostgreSQL
- **Migraciones/Tablas**: Se crean automáticamente al iniciar la app mediante SQLModel.
- **Seeding**: Ejecutá `python seed_data.py` para cargar datos de prueba.

---
Para ver la documentación completa del proyecto (incluyendo el frontend), consultá el [README principal](../README.md).
