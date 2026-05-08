from typing import List, Optional
from sqlmodel import Session, select
from .models import Ingrediente
from app.modules.productos.models import ProductoIngrediente

class IngredienteRepository:
    """
    REPOSITORIO DE INGREDIENTES
    Centraliza las operaciones de persistencia para el catálogo de ingredientes.
    """
    @staticmethod
    def create(session: Session, ingrediente: Ingrediente) -> None:
        """Agrega un ingrediente a la sesión (Delega el commit al Unit of Work)."""
        session.add(ingrediente)

    @staticmethod
    def get_all(session: Session, producto_id: Optional[int] = None) -> List[Ingrediente]:
        query = select(Ingrediente)
        if producto_id:
            query = query.join(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        return session.exec(query).all()

    @staticmethod
    def get_by_id(session: Session, ingrediente_id: int) -> Optional[Ingrediente]:
        return session.get(Ingrediente, ingrediente_id)

    @staticmethod
    def update(session: Session, ingrediente: Ingrediente) -> None:
        session.add(ingrediente)

    @staticmethod
    def delete(session: Session, ingrediente: Ingrediente) -> None:
        session.delete(ingrediente)
