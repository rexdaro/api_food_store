from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional

from app.db.database import get_session
from . import services
from .schemas import ProductoCreate, ProductoUpdate, ProductoRead

router = APIRouter()


@router.get("/", response_model=List[ProductoRead])
async def read_productos(
    categoria_id: Optional[int] = None, # <-- Nuevo parámetro opcional
    session: Session = Depends(get_session)
):
    """
    Lista los productos. Se puede filtrar por categoria_id enviándolo como parámetro.
    Ejemplo: /productos/?categoria_id=5
    """
    return services.get_productos(session, categoria_id=categoria_id)


@router.get("/inactivos", response_model=List[ProductoRead])
async def read_productos_inactivos(session: Session = Depends(get_session)):
    """
    Lista todos los productos inactivos (Módulo Productos).
    """
    return services.get_productos_inactivos(session)


@router.get("/{producto_id}", response_model=ProductoRead)
async def read_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Busca un producto por ID.
    """
    producto = services.get_producto_by_id(session, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoRead, status_code=201)
async def create_producto(
    producto_in: ProductoCreate, session: Session = Depends(get_session)
):
    """
    Crea un nuevo producto.
    """
    return services.create_producto(session, producto_in)


@router.patch("/{producto_id}", response_model=ProductoRead)
async def update_producto(
    producto_id: int,
    producto_in: ProductoUpdate,
    session: Session = Depends(get_session),
):
    """
    Actualiza parcialmente los datos de un producto.
    """
    producto_db = services.get_producto_by_id(session, producto_id)
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return services.update_producto(session, producto_db, producto_in)


@router.delete(
    "/{producto_id}", response_model=ProductoRead, summary="Borrado lógico de producto"
)
async def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Desactiva un producto (borrado lógico).
    """
    producto = services.get_producto_by_id(session, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.disponible:
        raise HTTPException(
            status_code=400, detail="El producto ya se encuentra desactivado"
        )

    services.delete_producto(session, producto)
    return producto
