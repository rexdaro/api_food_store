# app/modules/ingredientes/schemas.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class IngredienteBase(SQLModel):
    """Campos base para los ingredientes."""
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None)
    es_alergeno: bool = Field(default=False)

class IngredienteCreate(IngredienteBase):
    """DTO para crear un ingrediente."""
    pass

class IngredienteUpdate(SQLModel):
    """DTO para actualizar un ingrediente (PATCH)."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None

class IngredienteRead(IngredienteBase):
    """DTO para devolver los datos de un ingrediente."""
    id: int
    created_at: datetime
