# Registro centralizado de modelos (NestJS Module pattern)
# Importamos todos los modelos de los módulos para que SQLModel los registre en metadata

from app.modules.productos.models import Producto
from app.modules.categorias.models import Categoria
from app.modules.ingredientes.models import Ingrediente
from app.modules.producto_categoria.producto_categoria_model import ProductoCategoria
from app.modules.producto_ingrediente.producto_ingrediente_model import ProductoIngrediente

__all__ = [
    "Producto",
    "Categoria",
    "Ingrediente",
    "ProductoCategoria",
    "ProductoIngrediente",
]
