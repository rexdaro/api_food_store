# app/modules/producto_ingrediente/services.py
from sqlmodel import Session, select
from typing import List
from .producto_ingrediente_model import ProductoIngrediente
from .schemas import ProductoIngredienteCreate

def vincular_producto_ingrediente(session: Session, vinculacion_in: ProductoIngredienteCreate) -> ProductoIngrediente:
    """Vincula un producto con un ingrediente."""
    # Evitamos dependencias circulares importando adentro
    from app.modules.productos.models import Producto
    from app.modules.ingredientes.models import Ingrediente

    if not session.get(Producto, vinculacion_in.producto_id):
        raise ValueError(f"El producto con ID {vinculacion_in.producto_id} no existe")
    
    if not session.get(Ingrediente, vinculacion_in.ingrediente_id):
        raise ValueError(f"El ingrediente con ID {vinculacion_in.ingrediente_id} no existe")

    existente = session.get(ProductoIngrediente, (vinculacion_in.producto_id, vinculacion_in.ingrediente_id))
    if existente:
        return existente
        
    nueva_vinculacion = ProductoIngrediente.from_orm(vinculacion_in)
    session.add(nueva_vinculacion)
    session.commit()
    session.refresh(nueva_vinculacion)
    return nueva_vinculacion

def desvincular_producto_ingrediente(session: Session, producto_id: int, ingrediente_id: int) -> bool:
    """Elimina el vínculo entre un producto y un ingrediente."""
    vinculacion = session.get(ProductoIngrediente, (producto_id, ingrediente_id))
    if not vinculacion:
        return False
    session.delete(vinculacion)
    session.commit()
    return True

def get_ingredientes_de_producto(session: Session, producto_id: int) -> List[ProductoIngrediente]:
    """Lista todos los ingredientes vinculados a un producto."""
    return session.exec(select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)).all()
