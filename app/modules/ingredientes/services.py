from typing import List, Optional
from app.db.unit_of_work import UnitOfWork
from .models import Ingrediente
from .schemas import IngredienteCreate, IngredienteUpdate

"""
LÓGICA DE NEGOCIO - INGREDIENTES
Gestión del catálogo de insumos y materias primas.
"""

def create_ingrediente(uow: UnitOfWork, ingrediente_in: IngredienteCreate) -> Ingrediente:
    with uow:
        nuevo_ingrediente = Ingrediente(**ingrediente_in.model_dump())
        uow.ingredientes.create(uow.session, nuevo_ingrediente)
        uow.commit()
        uow.refresh(nuevo_ingrediente)
        return nuevo_ingrediente

def get_ingredientes(uow: UnitOfWork, producto_id: Optional[int] = None) -> List[Ingrediente]:
    return uow.ingredientes.get_all(uow.session, producto_id=producto_id)

def get_ingrediente_by_id(uow: UnitOfWork, ingrediente_id: int) -> Optional[Ingrediente]:
    return uow.ingredientes.get_by_id(uow.session, ingrediente_id)

def update_ingrediente(uow: UnitOfWork, ingrediente_db: Ingrediente, ingrediente_in: IngredienteUpdate) -> Ingrediente:
    with uow:
        datos = ingrediente_in.model_dump(exclude_unset=True)
        for campo, valor in datos.items():
            setattr(ingrediente_db, campo, valor)
        
        uow.ingredientes.update(uow.session, ingrediente_db)
        uow.commit()
        uow.refresh(ingrediente_db)
        return ingrediente_db

def delete_ingrediente(uow: UnitOfWork, ingrediente: Ingrediente) -> None:
    with uow:
        uow.ingredientes.delete(uow.session, ingrediente)
        uow.commit()
