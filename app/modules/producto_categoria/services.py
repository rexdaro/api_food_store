# app/modules/producto_categoria/services.py
from sqlmodel import Session, select
from typing import List
from .producto_categoria_model import ProductoCategoria
from .schemas import ProductoCategoriaCreate

def vincular_producto_categoria(session: Session, vinculacion_in: ProductoCategoriaCreate) -> ProductoCategoria:
    """
    Crea una relación entre un producto y una categoría.
    Si ya existe, la devuelve.
    """
    # Importamos adentro para evitar dependencias circulares
    from app.modules.productos.models import Producto
    from app.modules.categorias.models import Categoria

    # 1. Validamos que el producto exista
    if not session.get(Producto, vinculacion_in.producto_id):
        raise ValueError(f"El producto con ID {vinculacion_in.producto_id} no existe")
        
    # 2. Validamos que la categoría exista
    if not session.get(Categoria, vinculacion_in.categoria_id):
        raise ValueError(f"La categoría con ID {vinculacion_in.categoria_id} no existe")

    # 3. Verificamos si ya existe la relación para no duplicar
    existente = session.get(ProductoCategoria, (vinculacion_in.producto_id, vinculacion_in.categoria_id))
    if existente:
        return existente
        
    nueva_vinculacion = ProductoCategoria.from_orm(vinculacion_in)
    session.add(nueva_vinculacion)
    session.commit()
    session.refresh(nueva_vinculacion)
    return nueva_vinculacion

def desvincular_producto_categoria(session: Session, producto_id: int, categoria_id: int) -> bool:
    """
    Elimina la relación entre un producto y una categoría.
    """
    vinculacion = session.get(ProductoCategoria, (producto_id, categoria_id))
    if not vinculacion:
        return False
        
    session.delete(vinculacion)
    session.commit()
    return True

def get_vinculaciones_por_producto(session: Session, producto_id: int) -> List[ProductoCategoria]:
    """Lista todas las categorías de un producto."""
    return session.exec(select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)).all()
