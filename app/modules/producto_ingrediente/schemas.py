# app/modules/producto_ingrediente/schemas.py
from sqlmodel import SQLModel

class ProductoIngredienteBase(SQLModel):
    producto_id: int
    ingrediente_id: int
    es_removible: bool = False

class ProductoIngredienteCreate(ProductoIngredienteBase):
    """DTO para crear la relación producto-ingrediente."""
    pass

class ProductoIngredienteRead(ProductoIngredienteBase):
    """DTO para leer la relación."""
    pass
