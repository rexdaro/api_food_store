from sqlmodel import Session
from app.db.database import engine
from app.modules.productos.repositories import ProductoRepository
from app.modules.categorias.repositories import CategoriaRepository
from app.modules.ingredientes.repositories import IngredienteRepository

class UnitOfWork:
    """
    PATRÓN UNIT OF WORK (Unidad de Trabajo)
    Implementado como Context Manager para asegurar la atomicidad.
    """
    def __init__(self, session: Session):
        self.session = session
        self.productos = ProductoRepository()
        self.categorias = CategoriaRepository()
        self.ingredientes = IngredienteRepository()

    def __enter__(self):
        """Retorna la instancia al iniciar el bloque 'with'."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Finaliza la unidad de trabajo. 
        Si ocurre una excepción, hace rollback automático.
        """
        if exc_type is not None:
            self.rollback()
        # Nota: El commit se mantiene explícito en el service para mayor claridad 
        # sobre cuándo se confirma la operación de negocio.
        self.session.close()

    def commit(self):
        """Confirma todos los cambios realizados en los repositorios de forma atómica."""
        self.session.commit()

    def rollback(self):
        """Revierte cualquier cambio pendiente si ocurre un error."""
        self.session.rollback()

    def refresh(self, obj):
        """Recupera el estado actual del objeto desde la base de datos."""
        self.session.refresh(obj)

def get_uow():
    """Inyecta el Unit of Work en el router."""
    with Session(engine) as session:
        yield UnitOfWork(session)
