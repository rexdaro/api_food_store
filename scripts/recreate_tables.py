"""
Script para recrear las tablas desde cero.
CUIDADO: Borra todas las tablas existentes y las vuelve a crear.
Usar solo en desarrollo.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlmodel import SQLModel
from app.db.database import engine
import app.models


if __name__ == "__main__":
    print("Eliminando tablas existentes...")
    SQLModel.metadata.drop_all(engine)
    print("Creando tablas nuevas...")
    SQLModel.metadata.create_all(engine)
    print("Listo!")
