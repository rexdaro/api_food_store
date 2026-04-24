from fastapi import APIRouter
from app.modules.productos import router as productos_router
from app.modules.categorias import router as categorias_router
from app.modules.producto_categoria import router as producto_categoria_router
from app.modules.ingredientes import router as ingredientes_router
from app.modules.producto_ingrediente import router as producto_ingrediente_router

api_router = APIRouter()

# Unificamos todos los routers de los módulos aquí
api_router.include_router(productos_router.router, prefix="/productos", tags=["Productos"])
api_router.include_router(categorias_router.router, prefix="/categorias", tags=["Categorías"])
api_router.include_router(producto_categoria_router.router, prefix="/vinculos-categorias", tags=["Vínculos Producto-Categoría"])
api_router.include_router(ingredientes_router.router, prefix="/ingredientes", tags=["Ingredientes"])
api_router.include_router(producto_ingrediente_router.router, prefix="/vinculos-ingredientes", tags=["Vínculos Producto-Ingrediente"])
