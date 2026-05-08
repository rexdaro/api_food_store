from typing import Optional
from sqlmodel import Session, select, func
from .models import Producto, ProductoCategoria, ProductoIngrediente

class ProductoRepository:
    """
    PATRÓN REPOSITORY (Repositorio)
    
    Esta capa encapsula toda la lógica de acceso a datos (queries SQLModel/SQLAlchemy).
    Aísla la lógica de negocio de los detalles de la base de datos, permitiendo 
    que el Service se comunique con objetos de dominio en lugar de lidiar con el motor SQL.
    """
    @staticmethod
    def create(session: Session, producto: Producto) -> None:
        """Agrega un producto a la sesión. No confirma la transacción (delega al UoW)."""
        session.add(producto)

    @staticmethod
    def get_by_id(session: Session, producto_id: int) -> Optional[Producto]:
        return session.get(Producto, producto_id)

    @staticmethod
    def get_all(
        session: Session, 
        categoria_id: Optional[int] = None,
        search: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> dict:
        query = select(Producto)
        
        if only_active:
            query = query.where(Producto.disponible)
        else:
            query = query.where(~Producto.disponible)
        
        if categoria_id:
            query = query.join(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
        
        if search:
            query = query.where(
                (Producto.nombre.ilike(f"%{search}%")) | 
                (Producto.descripcion.ilike(f"%{search}%"))
            )
        
        total_query = select(func.count()).select_from(query.subquery())
        total = session.exec(total_query).one()
        items = session.exec(query.offset(offset).limit(limit)).all()
        
        return {"items": items, "total": total}

    @staticmethod
    def update(session: Session, producto: Producto) -> None:
        session.add(producto)
        # NO hay commit aquí

    @staticmethod
    def delete_logic(session: Session, producto: Producto) -> None:
        session.add(producto)
        # NO hay commit aquí

    # --- Relaciones ---

    @staticmethod
    def get_vinculacion_categoria(session: Session, producto_id: int, categoria_id: int) -> Optional[ProductoCategoria]:
        return session.get(ProductoCategoria, (producto_id, categoria_id))

    @staticmethod
    def save_vinculacion_categoria(session: Session, vinculacion: ProductoCategoria) -> None:
        session.add(vinculacion)

    @staticmethod
    def remove_vinculacion_categoria(session: Session, vinculacion: ProductoCategoria) -> None:
        session.delete(vinculacion)

    @staticmethod
    def get_vinculacion_ingrediente(session: Session, producto_id: int, ingrediente_id: int) -> Optional[ProductoIngrediente]:
        return session.get(ProductoIngrediente, (producto_id, ingrediente_id))

    @staticmethod
    def save_vinculacion_ingrediente(session: Session, vinculacion: ProductoIngrediente) -> None:
        session.add(vinculacion)

    @staticmethod
    def remove_vinculacion_ingrediente(session: Session, vinculacion: ProductoIngrediente) -> None:
        session.delete(vinculacion)
