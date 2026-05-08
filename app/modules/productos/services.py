from datetime import datetime
from typing import List, Optional
from app.db.unit_of_work import UnitOfWork
from .models import Producto, ProductoCategoria, ProductoIngrediente
from .schemas import (
    ProductoCreate, 
    ProductoUpdate, 
    ProductoCategoriaCreate, 
    ProductoIngredienteCreate
)

"""
CAPA DE SERVICIO (Domain Services)

Contiene la lógica de negocio pura de la aplicación. El Service orquestra 
las operaciones llamando a los Repositorios a través del Unit of Work (UoW). 
Es el encargado de decidir cuándo una operación de negocio es exitosa y 
debe confirmarse (commit) o fallida (rollback).
"""

def create_producto(uow: UnitOfWork, producto_in: ProductoCreate) -> Producto:
    with uow:
        nuevo_producto = Producto(**producto_in.model_dump(), disponible=True)
        uow.productos.create(uow.session, nuevo_producto)
        uow.commit()
        uow.refresh(nuevo_producto)
        return nuevo_producto

def get_productos(
    uow: UnitOfWork, 
    categoria_id: Optional[int] = None,
    search: Optional[str] = None,
    offset: int = 0,
    limit: int = 100
) -> dict:
    # Las lecturas no necesitan transaccionalidad, pero usamos el uow.session
    return uow.productos.get_all(
        uow.session, categoria_id, search, offset, limit, only_active=True
    )

def get_productos_inactivos(uow: UnitOfWork) -> List[Producto]:
    result = uow.productos.get_all(uow.session, only_active=False)
    return result["items"]

def get_producto_by_id(uow: UnitOfWork, producto_id: int) -> Optional[Producto]:
    return uow.productos.get_by_id(uow.session, producto_id)

def update_producto(
    uow: UnitOfWork, producto_db: Producto, producto_in: ProductoUpdate
) -> Producto:
    with uow:
        datos_nuevos = producto_in.model_dump(exclude_unset=True)
        for campo, valor in datos_nuevos.items():
            setattr(producto_db, campo, valor)
        
        uow.productos.update(uow.session, producto_db)
        uow.commit()
        uow.refresh(producto_db)
        return producto_db

def delete_producto(uow: UnitOfWork, producto: Producto) -> None:
    with uow:
        producto.disponible = False
        producto.deleted_at = datetime.now()
        uow.productos.delete_logic(uow.session, producto)
        uow.commit()

# ============================================================
# LÓGICA DE VINCULACIÓN (Atomicidad vía Unit of Work)
# Aquí coordinamos múltiples repositorios bajo una misma transacción.
# Si una vinculación falla, el UoW asegura que no se persista nada.
# ============================================================

def vincular_producto_categoria(uow: UnitOfWork, vinculacion_in: ProductoCategoriaCreate) -> ProductoCategoria:
    with uow:
        if not uow.productos.get_by_id(uow.session, vinculacion_in.producto_id):
            raise ValueError(f"El producto con ID {vinculacion_in.producto_id} no existe")
        
        if not uow.categorias.get_by_id(uow.session, vinculacion_in.categoria_id):
            raise ValueError(f"La categoría con ID {vinculacion_in.categoria_id} no existe")
            
        existente = uow.productos.get_vinculacion_categoria(
            uow.session, vinculacion_in.producto_id, vinculacion_in.categoria_id
        )
        if existente:
            return existente
            
        nueva = ProductoCategoria(**vinculacion_in.model_dump())
        uow.productos.save_vinculacion_categoria(uow.session, nueva)
        uow.commit()
        uow.refresh(nueva)
        return nueva

def desvincular_producto_categoria(uow: UnitOfWork, producto_id: int, categoria_id: int) -> bool:
    with uow:
        v = uow.productos.get_vinculacion_categoria(uow.session, producto_id, categoria_id)
        if not v:
            return False
        uow.productos.remove_vinculacion_categoria(uow.session, v)
        uow.commit()
        return True

def vincular_producto_ingrediente(uow: UnitOfWork, vinculacion_in: ProductoIngredienteCreate) -> ProductoIngrediente:
    with uow:
        if not uow.productos.get_by_id(uow.session, vinculacion_in.producto_id):
            raise ValueError(f"El producto con ID {vinculacion_in.producto_id} no existe")
            
        if not uow.ingredientes.get_by_id(uow.session, vinculacion_in.ingrediente_id):
            raise ValueError(f"El ingrediente con ID {vinculacion_in.ingrediente_id} no existe")
            
        existente = uow.productos.get_vinculacion_ingrediente(
            uow.session, vinculacion_in.producto_id, vinculacion_in.ingrediente_id
        )
        if existente:
            return existente
            
        nueva = ProductoIngrediente(**vinculacion_in.model_dump())
        uow.productos.save_vinculacion_ingrediente(uow.session, nueva)
        uow.commit()
        uow.refresh(nueva)
        return nueva

def desvincular_producto_ingrediente(uow: UnitOfWork, producto_id: int, ingrediente_id: int) -> bool:
    with uow:
        v = uow.productos.get_vinculacion_ingrediente(uow.session, producto_id, ingrediente_id)
        if not v:
            return False
        uow.productos.remove_vinculacion_ingrediente(uow.session, v)
        uow.commit()
        return True
