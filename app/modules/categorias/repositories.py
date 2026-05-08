from typing import List, Optional
from sqlmodel import Session, select
from .models import Categoria
from app.modules.productos.models import ProductoCategoria

class CategoriaRepository:
    """
    REPOSITORIO DE CATEGORÍAS
    Maneja la persistencia de las categorías, incluyendo la lógica de 
    jerarquías (parent_id) y disponibilidad.
    """
    @staticmethod
    def create(session: Session, categoria: Categoria) -> None:
        """Agrega la categoría a la sesión. El commit se realiza en la Unit of Work."""
        session.add(categoria)

    @staticmethod
    def get_by_id(session: Session, categoria_id: int) -> Optional[Categoria]:
        return session.get(Categoria, categoria_id)

    @staticmethod
    def get_all(session: Session, producto_id: Optional[int] = None, only_active: bool = True) -> List[Categoria]:
        query = select(Categoria)
        if only_active:
            query = query.where(Categoria.disponible)
        else:
            query = query.where(~Categoria.disponible)
        if producto_id:
            query = query.join(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        return session.exec(query).all()

    @staticmethod
    def update(session: Session, categoria: Categoria) -> None:
        session.add(categoria)

    @staticmethod
    def delete_logic(session: Session, categoria: Categoria) -> None:
        session.add(categoria)
