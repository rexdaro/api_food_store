import logging
import os
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Logger centralizado para la DB
logger = logging.getLogger("Database")

# Usamos la URL desde la configuración centralizada
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

def init_db():
    logger.info("Iniciando infraestructura de persistencia...")
    import app.models  # Registro de modelos
    SQLModel.metadata.create_all(engine)
    logger.info("Esquema de base de datos sincronizado correctamente.")

def get_session():
    return Session(engine)
