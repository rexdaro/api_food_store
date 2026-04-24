# app/modules/producto_categoria/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.db.database import get_session
from . import services
from .schemas import ProductoCategoriaCreate, ProductoCategoriaRead

router = APIRouter()

@router.post("/", response_model=ProductoCategoriaRead, status_code=201)
async def vincular_producto_con_categoria(
    vinculacion_in: ProductoCategoriaCreate, 
    session: Session = Depends(get_session)
):
    """
    Víncula un producto con una categoría (Relación Muchos a Muchos).
    """
    try:
        return services.vincular_producto_categoria(session, vinculacion_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/producto/{producto_id}", response_model=List[ProductoCategoriaRead])
async def listar_categorias_de_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Lista todos los vínculos de un producto específico.
    """
    return services.get_vinculaciones_por_producto(session, producto_id)

@router.delete("/{producto_id}/{categoria_id}")
async def desvincular_producto_de_categoria(
    producto_id: int, 
    categoria_id: int, 
    session: Session = Depends(get_session)
):
    """
    Elimina el vínculo entre un producto y una categoría.
    """
    borrado = services.desvincular_producto_categoria(session, producto_id, categoria_id)
    if not borrado:
        raise HTTPException(status_code=404, detail="El vínculo no existe")
    return {"message": "Vínculo eliminado correctamente"}
