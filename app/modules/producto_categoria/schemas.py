# app/modules/producto_categoria/schemas.py
from sqlmodel import SQLModel
from datetime import datetime

class ProductoCategoriaBase(SQLModel):
    producto_id: int
    categoria_id: int
    es_principal: bool = False

class ProductoCategoriaCreate(ProductoCategoriaBase):
    """Datos necesarios para crear la relación."""
    pass

class ProductoCategoriaRead(ProductoCategoriaBase):
    """Datos que devolvemos al consultar la relación."""
    created_at: datetime
