from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.db.unit_of_work import UnitOfWork, get_uow
from . import services
from .schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead

router = APIRouter()

"""
API ROUTER - CATEGORÍAS
Puntos de entrada para la gestión del árbol de categorías.
"""

@router.get("/", response_model=List[CategoriaRead])
async def read_categorias(
    producto_id: Optional[int] = None,
    uow: UnitOfWork = Depends(get_uow)
):
    return services.get_categorias(uow, producto_id=producto_id)

@router.get("/inactivos", response_model=List[CategoriaRead])
async def read_categorias_inactivas(uow: UnitOfWork = Depends(get_uow)):
    return services.get_categorias_inactivas(uow)

@router.get("/{categoria_id}", response_model=CategoriaRead)
async def read_categoria(categoria_id: int, uow: UnitOfWork = Depends(get_uow)):
    categoria = services.get_categoria_by_id(uow, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaRead, status_code=201)
async def create_categoria(categoria_in: CategoriaCreate, uow: UnitOfWork = Depends(get_uow)):
    return services.create_categoria(uow, categoria_in)

@router.patch("/{categoria_id}", response_model=CategoriaRead)
async def update_categoria(
    categoria_id: int, 
    categoria_in: CategoriaUpdate, 
    uow: UnitOfWork = Depends(get_uow)
):
    categoria_db = services.get_categoria_by_id(uow, categoria_id)
    if not categoria_db:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return services.update_categoria(uow, categoria_db, categoria_in)

@router.delete("/{categoria_id}", response_model=CategoriaRead)
async def delete_categoria(categoria_id: int, uow: UnitOfWork = Depends(get_uow)):
    categoria = services.get_categoria_by_id(uow, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if not categoria.disponible:
        raise HTTPException(status_code=400, detail="La categoría ya está desactivada")
        
    services.delete_categoria(uow, categoria)
    return categoria
