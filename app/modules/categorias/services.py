from datetime import datetime
from typing import List, Optional
from app.db.unit_of_work import UnitOfWork
from .models import Categoria
from .schemas import CategoriaCreate, CategoriaUpdate

"""
LÓGICA DE NEGOCIO - CATEGORÍAS
Orquestación de operaciones de categorías a través del Unit of Work.
"""

def create_categoria(uow: UnitOfWork, categoria_in: CategoriaCreate) -> Categoria:
    with uow:
        if categoria_in.parent_id:
            parent = uow.categorias.get_by_id(uow.session, categoria_in.parent_id)
            if not parent:
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail=f"La categoría padre con ID {categoria_in.parent_id} no existe.")

        nueva_categoria = Categoria(**categoria_in.model_dump(), disponible=True)
        uow.categorias.create(uow.session, nueva_categoria)
        uow.commit()
        uow.refresh(nueva_categoria)
        return nueva_categoria

def get_categorias(uow: UnitOfWork, producto_id: Optional[int] = None) -> List[Categoria]:
    return uow.categorias.get_all(uow.session, producto_id=producto_id, only_active=True)

def get_categorias_inactivas(uow: UnitOfWork) -> List[Categoria]:
    return uow.categorias.get_all(uow.session, only_active=False)

def get_categoria_by_id(uow: UnitOfWork, categoria_id: int) -> Optional[Categoria]:
    return uow.categorias.get_by_id(uow.session, categoria_id)

def update_categoria(uow: UnitOfWork, categoria_db: Categoria, categoria_in: CategoriaUpdate) -> Categoria:
    with uow:
        datos = categoria_in.model_dump(exclude_unset=True)

        if "parent_id" in datos and datos["parent_id"] is not None:
            if datos["parent_id"] == categoria_db.id:
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="Una categoría no puede ser su propio padre.")
                
            parent = uow.categorias.get_by_id(uow.session, datos["parent_id"])
            if not parent:
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail=f"La categoría padre con ID {datos['parent_id']} no existe.")

        for campo, valor in datos.items():
            setattr(categoria_db, campo, valor)
        
        uow.categorias.update(uow.session, categoria_db)
        uow.commit()
        uow.refresh(categoria_db)
        return categoria_db

def delete_categoria(uow: UnitOfWork, categoria: Categoria) -> None:
    with uow:
        categoria.disponible = False
        categoria.deleted_at = datetime.now()
        uow.categorias.delete_logic(uow.session, categoria)
        uow.commit()
