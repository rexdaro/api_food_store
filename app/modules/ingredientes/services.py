# app/modules/ingredientes/services.py
from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from .models import Ingrediente
from .schemas import IngredienteCreate, IngredienteUpdate
from app.modules.producto_ingrediente.producto_ingrediente_model import ProductoIngrediente

def create_ingrediente(session: Session, ingrediente_in: IngredienteCreate) -> Ingrediente:
    """Crea un nuevo ingrediente."""
    nuevo_ingrediente = Ingrediente.from_orm(ingrediente_in)
    session.add(nuevo_ingrediente)
    session.commit()
    session.refresh(nuevo_ingrediente)
    return nuevo_ingrediente

def get_ingredientes(session: Session, producto_id: Optional[int] = None) -> List[Ingrediente]:
    """Lista ingredientes, opcionalmente filtrados por producto_id."""
    query = select(Ingrediente)
    
    if producto_id:
        query = query.join(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        
    return session.exec(query).all()

def get_ingrediente_by_id(session: Session, ingrediente_id: int) -> Optional[Ingrediente]:
    """Busca un ingrediente por ID."""
    return session.get(Ingrediente, ingrediente_id)

def update_ingrediente(session: Session, ingrediente_db: Ingrediente, ingrediente_in: IngredienteUpdate) -> Ingrediente:
    """Actualización parcial de un ingrediente."""
    datos = ingrediente_in.dict(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(ingrediente_db, campo, valor)
    
    session.add(ingrediente_db)
    session.commit()
    session.refresh(ingrediente_db)
    return ingrediente_db

def delete_ingrediente(session: Session, ingrediente: Ingrediente) -> None:
    """Eliminación física de un ingrediente."""
    session.delete(ingrediente)
    session.commit()
