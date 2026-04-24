# app/modules/producto_categoria/producto_categoria_model.py
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
import sqlalchemy as sa

class ProductoCategoria(SQLModel, table=True):
    """
    ESTA ES LA TABLA 'PUENTE' (Relación Muchos a Muchos)
    
    Esta clase define la tabla intermedia que conecta Productos con Categorías.
    Se usa porque un Producto puede tener muchas Categorías y una Categoría 
    puede tener muchos Productos.
    """
    __tablename__ = "producto_categoria"

    # ============================================================
    # 1. IDENTIDAD DE LA RELACIÓN (Foreign Keys)
    # ============================================================
    
    # Conexión con el Producto:
    # - sa.ForeignKey("producto.id"): El ID debe existir en la tabla 'producto'.
    # - primary_key=True: Este campo forma parte de la clave única de la fila.
    producto_id: int = Field(
        sa_column=sa.Column(
            sa.BigInteger, 
            sa.ForeignKey("producto.id"), 
            primary_key=True
        )
    )

    # Conexión con la Categoría:
    # - sa.ForeignKey("categoria.id"): El ID debe existir en la tabla 'categoria'.
    # - primary_key=True: Junto con producto_id, aseguran que no haya duplicados.
    categoria_id: int = Field(
        sa_column=sa.Column(
            sa.BigInteger, 
            sa.ForeignKey("categoria.id"), 
            primary_key=True
        )
    )

    # ============================================================
    # 2. ATRIBUTOS PROPIOS DEL VÍNCULO
    # ============================================================
    
    # Indica si esta es la categoría principal del producto (para mostrar en el catálogo).
    es_principal: bool = Field(default=False)

    # ============================================================
    # 3. AUDITORÍA
    # ============================================================
    
    # Fecha y hora en la que se creó esta asociación.
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now()
        )
    )
