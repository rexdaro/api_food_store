import logging
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Logger centralizado para la DB
logger = logging.getLogger("Database")

# INFRAESTRUCTURA DE PERSISTENCIA
# Configuramos el motor (engine) de SQLModel/SQLAlchemy que se conecta a PostgreSQL.
#settings.DATABASE_URL contiene el string de conexión (usuario, pass, host, db).
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def init_db():
    """
    SINCRONIZACIÓN DE ESQUEMA
    Registra todos los modelos importados en el metadata de SQLModel y crea 
    las tablas en la base de datos si no existen.
    """
    logger.info("Iniciando infraestructura de persistencia...")
    import app.models  # noqa: F401 (Registro de modelos en metadata)

    SQLModel.metadata.create_all(engine)
    logger.info("Esquema de base de datos sincronizado correctamente.")


def get_session():
    with Session(engine) as session:
        yield session
