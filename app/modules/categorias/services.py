from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from .models import Categoria
from .schemas import CategoriaCreate, CategoriaUpdate
from app.modules.producto_categoria.producto_categoria_model import ProductoCategoria

def create_categoria(session: Session, categoria_in: CategoriaCreate) -> Categoria:
    """
    Registra una nueva categoría. Valida que el padre exista si se proporciona.
    """
    # Validamos jerarquía si viene un parent_id
    if categoria_in.parent_id:
        parent = get_categoria_by_id(session, categoria_in.parent_id)
        if not parent:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400, 
                detail=f"La categoría padre con ID {categoria_in.parent_id} no existe."
            )

    nueva_categoria = Categoria(**categoria_in.dict(), disponible=True)
    
    try:
        session.add(nueva_categoria)
        session.commit()
        session.refresh(nueva_categoria)
        return nueva_categoria
    except Exception as e:
        session.rollback()
        raise e

def get_categorias(session: Session, producto_id: Optional[int] = None) -> List[Categoria]:
    """
    Retorna solo las categorías activas. Opcionalmente filtra por producto_id.
    """
    query = select(Categoria).where(Categoria.disponible)
    
    if producto_id:
        # Filtramos categorías asociadas al producto
        query = query.join(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        
    return session.exec(query).all()

def get_categorias_inactivas(session: Session) -> List[Categoria]:
    """
    Retorna la lista de categorías que han sido borradas lógicamente.
    """
    return session.exec(select(Categoria).where(~Categoria.disponible)).all()

def get_categoria_by_id(session: Session, categoria_id: int) -> Optional[Categoria]:
    """
    Busca una categoría por su ID.
    """
    return session.get(Categoria, categoria_id)

def update_categoria(session: Session, categoria_db: Categoria, categoria_in: CategoriaUpdate) -> Categoria:
    """
    Actualiza parcialmente los datos de una categoría. Valida el nuevo padre si cambia.
    """
    datos = categoria_in.dict(exclude_unset=True)

    # Si se intenta cambiar el padre, validamos que exista
    if "parent_id" in datos and datos["parent_id"] is not None:
        if datos["parent_id"] == categoria_db.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Una categoría no puede ser su propio padre.")
            
        parent = get_categoria_by_id(session, datos["parent_id"])
        if not parent:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400, 
                detail=f"La categoría padre con ID {datos['parent_id']} no existe."
            )

    for campo, valor in datos.items():
        setattr(categoria_db, campo, valor)
    
    try:
        session.add(categoria_db)
        session.commit()
        session.refresh(categoria_db)
        return categoria_db
    except Exception as e:
        session.rollback()
        raise e

def delete_categoria(session: Session, categoria: Categoria) -> None:
    """
    Borrado lógico: desactiva la categoría.
    """
    categoria.disponible = False
    categoria.deleted_at = datetime.now()
    session.add(categoria)
    session.commit()
