from sqlmodel import Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa

# Tabla intermedia
from app.modules.productos.models import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.models import Producto

from .schemas import CategoriaBase

class Categoria(CategoriaBase, table=True):
    """
    Representa la tabla 'categoria' en la base de datos.
    Soporta jerarquías (una categoría puede tener un padre) y borrado lógico.
    """
    id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(sa.BigInteger, primary_key=True, autoincrement=True),
    )
    
    # Campo para borrado lógico
    disponible: bool = Field(default=True)

    # FK para la auto-relación (Jerarquía)
    # Sobrescribimos el campo del Schema para agregarle la restricción de base de datos (ForeignKey)
    parent_id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(sa.BigInteger, sa.ForeignKey("categoria.id"), nullable=True),
    )

    # ---- Audit (campos de auditoría) ----
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True)),
    )

    # ---- Relaciones ----
    # Muchos a muchos con Producto
    productos: List["Producto"] = Relationship(
        back_populates="categorias", 
        link_model=ProductoCategoria
    )
    
    # Auto-relación (Jerarquía: ej. Ropa -> Ropa de Hombre)
    parent: Optional["Categoria"] = Relationship(
        back_populates="children", 
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )
    children: List["Categoria"] = Relationship(back_populates="parent")
