import sys
import os

# Agregamos la carpeta raíz al path para que Python encuentre el módulo 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from app.db.database import engine
# Importamos todos los modelos para que SQLModel los registre en la metadata
import app.models  # noqa: F401

def reset_db():
    print("ATENCION: Se van a borrar todos los datos de la base de datos.")
    confirm = input("¿Estas seguro? (s/n): ")
    
    if confirm.lower() == 's':
        print("Eliminando tablas existentes...")
        SQLModel.metadata.drop_all(engine)
        
        print("Creando tablas con la nueva estructura...")
        SQLModel.metadata.create_all(engine)
        
        print("Base de datos reseteada con exito.")
    else:
        print("Operacion cancelada.")

if __name__ == "__main__":
    reset_db()
