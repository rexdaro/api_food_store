from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa

# Tabla intermedia
from app.modules.productos.models import ProductoIngrediente

if TYPE_CHECKING:
    from app.modules.productos.models import Producto

class Ingrediente(SQLModel, table=True):
    # PK
    id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(sa.BigInteger, primary_key=True, autoincrement=True),
    )

    # Atributos
    nombre: str = Field(
        max_length=100, sa_column=sa.Column(sa.String(100), nullable=False, unique=True)
    )
    descripcion: Optional[str] = Field(default=None, sa_column=sa.Column(sa.Text))
    es_alergeno: bool = Field(
        default=False, sa_column=sa.Column(sa.Boolean, nullable=False)
    )

    # ---- Relaciones ----
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes", 
        link_model=ProductoIngrediente
    )

    # Audit
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )
