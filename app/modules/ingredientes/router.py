from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.db.unit_of_work import UnitOfWork, get_uow
from . import services
from .schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead

router = APIRouter()

@router.get("/", response_model=List[IngredienteRead])
async def read_ingredientes(
    producto_id: Optional[int] = None,
    uow: UnitOfWork = Depends(get_uow)
):
    return services.get_ingredientes(uow, producto_id=producto_id)

@router.get("/{ingrediente_id}", response_model=IngredienteRead)
async def read_ingrediente(ingrediente_id: int, uow: UnitOfWork = Depends(get_uow)):
    ingrediente = services.get_ingrediente_by_id(uow, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@router.post("/", response_model=IngredienteRead, status_code=201)
async def create_ingrediente(ingrediente_in: IngredienteCreate, uow: UnitOfWork = Depends(get_uow)):
    return services.create_ingrediente(uow, ingrediente_in)

@router.patch("/{ingrediente_id}", response_model=IngredienteRead)
async def update_ingrediente(
    ingrediente_id: int, 
    ingrediente_in: IngredienteUpdate, 
    uow: UnitOfWork = Depends(get_uow)
):
    ingrediente_db = services.get_ingrediente_by_id(uow, ingrediente_id)
    if not ingrediente_db:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return services.update_ingrediente(uow, ingrediente_db, ingrediente_in)

@router.delete("/{ingrediente_id}")
async def delete_ingrediente(ingrediente_id: int, uow: UnitOfWork = Depends(get_uow)):
    ingrediente = services.get_ingrediente_by_id(uow, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    services.delete_ingrediente(uow, ingrediente)
    return {"message": "Ingrediente eliminado correctamente"}
