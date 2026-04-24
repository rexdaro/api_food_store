import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import engine
from sqlmodel import SQLModel
import app.models


def create_tables():
    print("Conectando a PostgreSQL y creando tablas... 🐘")
    try:
        SQLModel.metadata.create_all(engine)
        print("¡Tablas creadas con éxito en 'proyecto_programacion'! ✅")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")


if __name__ == "__main__":
    create_tables()
