from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional

from app.db.database import get_session
from . import services
from .schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead

router = APIRouter()

@router.get("/", response_model=List[CategoriaRead])
async def read_categorias(
    producto_id: Optional[int] = None, # <-- Parámetro opcional
    session: Session = Depends(get_session)
):
    """
    Lista todas las categorías activas. 
    Se puede filtrar por producto_id para ver las categorías de un producto.
    """
    return services.get_categorias(session, producto_id=producto_id)

@router.get("/inactivos", response_model=List[CategoriaRead])
async def read_categorias_inactivas(session: Session = Depends(get_session)):
    """
    Lista todas las categorías que están marcadas como inactivas (borrado lógico).
    """
    return services.get_categorias_inactivas(session)

@router.get("/{categoria_id}", response_model=CategoriaRead)
async def read_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """
    Obtiene el detalle de una categoría específica.
    """
    categoria = services.get_categoria_by_id(session, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaRead, status_code=201)
async def create_categoria(categoria_in: CategoriaCreate, session: Session = Depends(get_session)):
    """
    Crea una nueva categoría.
    """
    return services.create_categoria(session, categoria_in)

@router.patch("/{categoria_id}", response_model=CategoriaRead)
async def update_categoria(
    categoria_id: int, 
    categoria_in: CategoriaUpdate, 
    session: Session = Depends(get_session)
):
    """
    Modifica parcialmente una categoría.
    """
    categoria_db = services.get_categoria_by_id(session, categoria_id)
    if not categoria_db:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return services.update_categoria(session, categoria_db, categoria_in)

@router.delete("/{categoria_id}", response_model=CategoriaRead)
async def delete_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """
    Realiza el borrado lógico de una categoría.
    """
    categoria = services.get_categoria_by_id(session, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if not categoria.disponible:
        raise HTTPException(status_code=400, detail="La categoría ya está desactivada")
        
    services.delete_categoria(session, categoria)
    return categoria
