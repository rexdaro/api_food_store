from sqlmodel import Session
from app.db.database import engine
from app.modules.productos.repositories import ProductoRepository
from app.modules.categorias.repositories import CategoriaRepository
from app.modules.ingredientes.repositories import IngredienteRepository

class UnitOfWork:
    """
    PATRÓN UNIT OF WORK (Unidad de Trabajo)
    
    Este patrón coordina el trabajo de múltiples repositorios compartiendo una única 
    sesión de base de datos. Su objetivo principal es garantizar la ATOMICIDAD (ACID):
    o todas las operaciones de un flujo de negocio se confirman (commit), 
    o ninguna se aplica (rollback).
    """
    def __init__(self, session: Session):
        # La sesión es inyectada para asegurar que todos los repositorios 
        # operen dentro de la misma transacción.
        self.session = session
        self.productos = ProductoRepository()
        self.categorias = CategoriaRepository()
        self.ingredientes = IngredienteRepository()

    def commit(self):
        """Confirma todos los cambios realizados en los repositorios de forma atómica."""
        self.session.commit()

    def rollback(self):
        """Revierte cualquier cambio pendiente si ocurre un error en el flujo de negocio."""
        self.session.rollback()

    def refresh(self, obj):
        """Recupera el estado actual del objeto desde la base de datos (ej: IDs autogenerados)."""
        self.session.refresh(obj)

def get_uow():
    """
    GENERADOR DE DEPENDENCIA
    Utilizado por FastAPI para inyectar una instancia fresca de UoW en cada petición,
    asegurando un manejo correcto del ciclo de vida de la sesión.
    """
    with Session(engine) as session:
        yield UnitOfWork(session)
