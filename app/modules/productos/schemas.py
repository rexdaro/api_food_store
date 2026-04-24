from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
import sqlalchemy as sa

class ProductoBase(SQLModel):
    """Campos compartidos entre creación, lectura y base de datos."""
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = Field(
        default=None, sa_column=sa.Column(sa.Text)
    )
    precio_base: Decimal = Field(
        sa_column=sa.Column(sa.Numeric(10, 2), nullable=False)
    )
    stock_cantidad: int = Field(default=0)
    imagenes_url: Optional[list[str]] = Field(
        default=None, sa_column=sa.Column(sa.ARRAY(sa.Text))
    )

class ProductoCreate(ProductoBase):
    """
    ESTE ES TU DTO (Data Transfer Object).
    Se usa para que el cliente (frontend/web) nos mande SOLO los datos 
    necesarios para CREAR un producto. 
    """
    pass

class ProductoUpdate(SQLModel):
    """
    DTO para PATCH. 
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    nombre: Optional[str] = Field(default=None, max_length=150)
    descripcion: Optional[str] = Field(default=None)
    precio_base: Optional[Decimal] = Field(default=None)
    stock_cantidad: Optional[int] = Field(default=None)
    imagenes_url: Optional[list[str]] = Field(default=None)

class ProductoRead(ProductoBase):
    """
    DTO para salida. Lo que el servidor devuelve al cliente.
    """
    id: int
    disponible: bool
