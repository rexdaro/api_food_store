from sqlmodel import SQLModel, Field
from typing import Optional


class CategoriaBase(SQLModel):
    """
    Clase base con los campos que comparten todos los esquemas de Categoria.
    """

    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(
        default=None, description="Descripción de la categoría"
    )
    imagen_url: Optional[str] = Field(default=None)
    parent_id: Optional[int] = Field(
        default=None,
        description="ID de la categoría padre. Usar null para categorías principales. "
        "Si se indica un ID, será una subcategoría de ese padre.",
    )


class CategoriaCreate(CategoriaBase):
    """
    DTO para crear una categoría.
    Es lo que el cliente manda por POST.
    """

    pass


class CategoriaUpdate(SQLModel):
    """
    DTO para actualizar una categoría (PATCH).
    Todos los campos son opcionales.
    """

    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = Field(default=None)
    imagen_url: Optional[str] = Field(default=None)
    parent_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de categoría padre para moverla de lugar en la jerarquía.",
    )


class CategoriaRead(CategoriaBase):
    """
    DTO para devolver datos al cliente.
    Incluye ID y estado de disponibilidad.
    """

    id: int
    disponible: bool
