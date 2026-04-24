from sqlmodel import Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa

# Tablas intermedias (No causan circular imports)
from app.modules.producto_categoria.producto_categoria_model import ProductoCategoria
from app.modules.producto_ingrediente.producto_ingrediente_model import ProductoIngrediente

if TYPE_CHECKING:
    from app.modules.categorias.models import Categoria
    from app.modules.ingredientes.models import Ingrediente


from .schemas import ProductoBase

# ============================================================
# MODELO - Define la tabla "producto" en la base de datos
# ============================================================


class Producto(ProductoBase, table=True):
    __table_args__ = (
        sa.CheckConstraint("precio_base >= 0", name="ck_producto_precio_base"),
        sa.CheckConstraint("stock_cantidad >= 0", name="ck_producto_stock_cantidad"),
    )

    id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(sa.BigInteger, primary_key=True, autoincrement=True),
    )

    disponible: bool = Field(default=True)

    # ---- Audit (campos de auditoría) ----
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None, sa_column=sa.Column(sa.DateTime(timezone=True))
    )

    # ---- Relaciones (Hacen que el código sea un placer de leer) ----
    # link_model: apunta a la clase de la tabla intermedia (muchos a muchos)
    categorias: List["Categoria"] = Relationship(
        back_populates="productos", link_model=ProductoCategoria
    )

    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="productos", link_model=ProductoIngrediente
    )
