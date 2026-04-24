# app/modules/producto_ingrediente/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.db.database import get_session
from . import services
from .schemas import ProductoIngredienteCreate, ProductoIngredienteRead

router = APIRouter()

@router.post("/", response_model=ProductoIngredienteRead, status_code=201)
async def vincular_producto_con_ingrediente(
    vinculacion_in: ProductoIngredienteCreate, 
    session: Session = Depends(get_session)
):
    """Asocia un producto con un ingrediente."""
    try:
        return services.vincular_producto_ingrediente(session, vinculacion_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/producto/{producto_id}", response_model=List[ProductoIngredienteRead])
async def listar_ingredientes_de_producto(producto_id: int, session: Session = Depends(get_session)):
    """Lista todos los ingredientes de un producto."""
    return services.get_ingredientes_de_producto(session, producto_id)

@router.delete("/{producto_id}/{ingrediente_id}")
async def desvincular_producto_de_ingrediente(
    producto_id: int, 
    ingrediente_id: int, 
    session: Session = Depends(get_session)
):
    """Elimina el vínculo entre un producto y un ingrediente."""
    borrado = services.desvincular_producto_ingrediente(session, producto_id, ingrediente_id)
    if not borrado:
        raise HTTPException(status_code=404, detail="El vínculo no existe")
    return {"message": "Ingrediente desvinculado correctamente"}
