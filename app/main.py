import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db, logger
from app.core.config import settings

# IMPORTANTE: Registramos los modelos antes que los routers
# Esto evita el error "failed to locate a name ('Producto')"
import app.models  

from app.api.v1.api import api_router


# 1. LIFESPAN: Tareas que ocurren antes de que el servidor acepte pedidos
# (Como el ApplicationContext de Spring)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Iniciando servidor: {settings.PROJECT_NAME}")
    try:
        init_db()  # Sincronizamos la base de datos
        logger.info("Base de datos sincronizada y lista.")
    except Exception as e:
        logger.error(f"Error crítico en el arranque: {e}")
        # Aquí podrías decidir si frenar el server o no

    yield  # Aquí es donde el servidor se queda "escuchando" pedidos

    logger.info("🛑 Apagando servidor...")


# 2. INSTANCIA DE LA APP
app = FastAPI(
    title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan
)

# 3. CONFIGURACIÓN DE CORS (Permisos para el Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitimos todos los orígenes en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Permitimos todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitimos todos los encabezados
)


# 3. ROUTERS (NestJS Style)
app.include_router(api_router, prefix="/api/v1")


# 4. HEALTH CHECK
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "message": f"Bienvenido a {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
    }


# 4. PUNTO DE ENTRADA (Simula el mvn spring-boot:run)
if __name__ == "__main__":
    logger.info(f"Servidor configurado en: http://{settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG
    )
