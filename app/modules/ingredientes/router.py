# app/modules/ingredientes/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional
from app.db.database import get_session
from . import services
from .schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead

router = APIRouter()

@router.get("/", response_model=List[IngredienteRead])
async def read_ingredientes(
    producto_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """Lista todos los ingredientes. Permite filtrar por producto_id."""
    return services.get_ingredientes(session, producto_id=producto_id)

@router.get("/{ingrediente_id}", response_model=IngredienteRead)
async def read_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    """Obtiene el detalle de un ingrediente."""
    ingrediente = services.get_ingrediente_by_id(session, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@router.post("/", response_model=IngredienteRead, status_code=201)
async def create_ingrediente(ingrediente_in: IngredienteCreate, session: Session = Depends(get_session)):
    """Crea un nuevo ingrediente."""
    return services.create_ingrediente(session, ingrediente_in)

@router.patch("/{ingrediente_id}", response_model=IngredienteRead)
async def update_ingrediente(
    ingrediente_id: int, 
    ingrediente_in: IngredienteUpdate, 
    session: Session = Depends(get_session)
):
    """Actualiza parcialmente un ingrediente."""
    ingrediente_db = services.get_ingrediente_by_id(session, ingrediente_id)
    if not ingrediente_db:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return services.update_ingrediente(session, ingrediente_db, ingrediente_in)

@router.delete("/{ingrediente_id}")
async def delete_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    """Elimina un ingrediente."""
    ingrediente = services.get_ingrediente_by_id(session, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    services.delete_ingrediente(session, ingrediente)
    return {"message": "Ingrediente eliminado correctamente"}
