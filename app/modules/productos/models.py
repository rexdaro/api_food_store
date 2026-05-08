from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from .schemas import ProductoBase

# ============================================================
# TABLAS DE VINCULACIÓN (Junction Tables)
# Se centralizan aquí para simplificar la gestión de relaciones M:N
# entre Productos, Categorías e Ingredientes.
# ============================================================

class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"
    producto_id: int = Field(
        sa_column=sa.Column(sa.BigInteger, sa.ForeignKey("producto.id"), primary_key=True)
    )
    categoria_id: int = Field(
        sa_column=sa.Column(sa.BigInteger, sa.ForeignKey("categoria.id"), primary_key=True)
    )
    es_principal: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )

class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"
    producto_id: int = Field(
        sa_column=sa.Column(sa.BigInteger, sa.ForeignKey("producto.id"), primary_key=True)
    )
    ingrediente_id: int = Field(
        sa_column=sa.Column(sa.BigInteger, sa.ForeignKey("ingrediente.id"), primary_key=True)
    )
    es_removible: bool = Field(default=False)


if TYPE_CHECKING:
    from app.modules.categorias.models import Categoria
    from app.modules.ingredientes.models import Ingrediente




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
