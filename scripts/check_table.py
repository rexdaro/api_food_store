import sys
import os

# Añade el directorio raíz al path para que reconozca el paquete 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlmodel import Session, text
from app.db.database import engine

with Session(engine) as session:
    # Verificar tabla producto_categoria
    result = session.exec(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='producto_categoria'")
    )
    rows = result.all()
    if rows:
        print("Tabla 'producto_categoria' EXISTE")
        # Chequear PK compuesta
        result_pk = session.exec(
            text("""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = 'producto_categoria'
            """)
        )
        pks = result_pk.all()
        print(f"PK compuesta por: {[p[0] for p in pks]}")
    else:
        print("Tabla 'producto_categoria' NO existe")
