from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Annotated

from app.db.unit_of_work import UnitOfWork, get_uow
from . import services
from .schemas import (
    ProductoCreate, 
    ProductoUpdate, 
    ProductoRead, 
    ProductoPaginated,
    ProductoCategoriaCreate,
    ProductoCategoriaRead,
    ProductoIngredienteCreate,
    ProductoIngredienteRead
)

router = APIRouter()

"""
CAPA DE TRANSPORTE (API Routers)

Define los puntos de entrada (endpoints) de la aplicación. Su única responsabilidad 
es recibir peticiones HTTP, validar schemas y delegar la ejecución a la capa de servicio.
Utiliza INYECCIÓN DE DEPENDENCIAS (Depends) para obtener una instancia del Unit of Work.
"""

@router.get("/", response_model=ProductoPaginated)
async def read_productos(
    uow: UnitOfWork = Depends(get_uow),
    categoria_id: Annotated[
        Optional[int], 
        Query(description="Filtrar por el ID de la categoría")
    ] = None,
    offset: Annotated[
        int, 
        Query(ge=0, description="Número de registros a saltar")
    ] = 0,
    limit: Annotated[
        int, 
        Query(ge=1, le=100, description="Máximo de registros a retornar")
    ] = 100,
    search: Annotated[
        Optional[str], 
        Query(description="Buscar por nombre o descripción")
    ] = None,
):
    return services.get_productos(
        uow, 
        categoria_id=categoria_id, 
        search=search,
        offset=offset, 
        limit=limit
    )


@router.get("/inactivos", response_model=List[ProductoRead])
async def read_productos_inactivos(uow: UnitOfWork = Depends(get_uow)):
    return services.get_productos_inactivos(uow)


@router.get("/{producto_id}", response_model=ProductoRead)
async def read_producto(producto_id: int, uow: UnitOfWork = Depends(get_uow)):
    producto = services.get_producto_by_id(uow, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoRead, status_code=201)
async def create_producto(
    producto_in: ProductoCreate, uow: UnitOfWork = Depends(get_uow)
):
    return services.create_producto(uow, producto_in)


@router.patch("/{producto_id}", response_model=ProductoRead)
async def update_producto(
    producto_id: int,
    producto_in: ProductoUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    producto_db = services.get_producto_by_id(uow, producto_id)
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return services.update_producto(uow, producto_db, producto_in)


@router.delete(
    "/{producto_id}", response_model=ProductoRead, summary="Borrado lógico de producto"
)
async def delete_producto(producto_id: int, uow: UnitOfWork = Depends(get_uow)):
    producto = services.get_producto_by_id(uow, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.disponible:
        raise HTTPException(
            status_code=400, detail="El producto ya se encuentra desactivado"
        )

    services.delete_producto(uow, producto)
    return producto


# ============================================================
# VINCULACIÓN
# ============================================================

@router.post("/vincular-categoria", response_model=ProductoCategoriaRead)
async def vincular_categoria(
    vinculacion: ProductoCategoriaCreate, uow: UnitOfWork = Depends(get_uow)
):
    try:
        return services.vincular_producto_categoria(uow, vinculacion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/desvincular-categoria/{producto_id}/{categoria_id}")
async def desvincular_categoria(
    producto_id: int, categoria_id: int, uow: UnitOfWork = Depends(get_uow)
):
    if not services.desvincular_producto_categoria(uow, producto_id, categoria_id):
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Desvinculación exitosa"}

@router.post("/vincular-ingrediente", response_model=ProductoIngredienteRead)
async def vincular_ingrediente(
    vinculacion: ProductoIngredienteCreate, uow: UnitOfWork = Depends(get_uow)
):
    try:
        return services.vincular_producto_ingrediente(uow, vinculacion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/desvincular-ingrediente/{producto_id}/{ingrediente_id}")
async def desvincular_ingrediente(
    producto_id: int, ingrediente_id: int, uow: UnitOfWork = Depends(get_uow)
):
    if not services.desvincular_producto_ingrediente(uow, producto_id, ingrediente_id):
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Desvinculación exitosa"}
