import os
from dotenv import load_dotenv

# Cargamos las variables del ARCHIVO .env
load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("APP_NAME", "Proyecto Programacion")
    PROJECT_VERSION: str = "1.0.0"

    # Base de Datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Servidor
    HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Debug
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


# Instancia única de configuración (Singleton)
settings = Settings()
