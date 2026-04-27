from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select, func
from .models import Producto
from .schemas import ProductoCreate, ProductoUpdate
from app.modules.producto_categoria.producto_categoria_model import ProductoCategoria


def create_producto(session: Session, producto_in: ProductoCreate) -> Producto:
    """
    Crea un nuevo producto en la base de datos.
    Se inicializa como disponible por defecto.
    """
    nuevo_producto = Producto(**producto_in.dict(), disponible=True)
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto

def get_productos(
    session: Session, 
    categoria_id: Optional[int] = None,
    search: Optional[str] = None,
    offset: int = 0,
    limit: int = 100
) -> dict:
    """
    Retorna la lista de productos disponibles con soporte para paginación y filtros,
    junto con el conteo total para la UI.
    """
    query = select(Producto).where(Producto.disponible)
    
    if categoria_id:
        query = query.join(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
    
    if search:
        query = query.where(
            (Producto.nombre.ilike(f"%{search}%")) | 
            (Producto.descripcion.ilike(f"%{search}%"))
        )
    
    # Obtenemos el total antes de aplicar offset/limit
    total_query = select(func.count()).select_from(query.subquery())
    total = session.exec(total_query).one()
    
    # Obtenemos los items de la página actual
    items = session.exec(query.offset(offset).limit(limit)).all()
    
    return {"items": items, "total": total}


def get_productos_inactivos(session: Session) -> List[Producto]:
    """
    Retorna la lista de productos que han sido borrados lógicamente.
    """
    return session.exec(select(Producto).where(~Producto.disponible)).all()


def get_producto_by_id(session: Session, producto_id: int) -> Optional[Producto]:
    """
    Busca un producto por su clave primaria.
    """
    return session.get(Producto, producto_id)


def update_producto(
    session: Session, producto_db: Producto, producto_in: ProductoUpdate
) -> Producto:
    """
    Actualiza parcialmente los campos de un producto existente.
    """
    datos_nuevos = producto_in.dict(exclude_unset=True)

    for campo, valor in datos_nuevos.items():
        setattr(producto_db, campo, valor)

    session.add(producto_db)
    session.commit()
    session.refresh(producto_db)
    return producto_db


def delete_producto(session: Session, producto: Producto) -> None:
    """
    Realiza un borrado lógico marcando el producto como no disponible.
    """
    producto.disponible = False
    producto.deleted_at = datetime.now()

    session.add(producto)
    session.commit()
