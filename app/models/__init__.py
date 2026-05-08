# Este archivo registra todos los modelos en el metadata de SQLModel.
# Es importado por main.py y database.py ANTES de llamar a create_all(),
# garantizando que las tablas se creen en el orden correcto.

# Productos (primero, porque contiene las tablas intermedias)
from app.modules.productos.models import Producto, ProductoCategoria, ProductoIngrediente  # noqa: F401

# Categorías e Ingredientes (dependen de las tablas intermedias de productos)
from app.modules.categorias.models import Categoria  # noqa: F401
from app.modules.ingredientes.models import Ingrediente  # noqa: F401
