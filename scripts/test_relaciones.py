# test_relaciones.py
import logging
from sqlmodel import Session, select
from app.db.database import engine, init_db
from app.modules.productos.models import Producto
from app.modules.categorias.models import Categoria

# Configuramos logging básico para ver qué pasa
logging.basicConfig(level=logging.INFO)

def probar_muchos_a_muchos():
    # 1. Aseguramos que las tablas existan (esto crea las tablas si no existen)
    print("\n[1/5] Sincronizando base de datos...")
    init_db()

    with Session(engine) as session:
        # 2. Buscamos o creamos una categoría
        categoria = session.exec(select(Categoria).where(Categoria.nombre == "Bebidas")).first()
        if not categoria:
            print("[2/5] Creando categoría 'Bebidas'...")
            categoria = Categoria(nombre="Bebidas", descripcion="Todo tipo de refrescos")
            session.add(categoria)
        else:
            print("[2/5] La categoría 'Bebidas' ya existe.")
        
        # 3. Buscamos o creamos un producto
        producto = session.exec(select(Producto).where(Producto.nombre == "Coca Cola")).first()
        if not producto:
            print("[3/5] Creando producto 'Coca Cola'...")
            producto = Producto(
                nombre="Coca Cola", 
                precio_base=1500.00, 
                stock_cantidad=50
            )
            session.add(producto)
        else:
            print("[3/5] El producto 'Coca Cola' ya existe.")

        session.commit()
        session.refresh(categoria)
        session.refresh(producto)

        # 4. LA MAGIA: Asociamos el producto con la categoría
        # Como definimos la relación con link_model en el modelo Producto,
        # solo tenemos que agregar la categoría a la lista 'categorias' del producto.
        if categoria not in producto.categorias:
            print(f"[4/5] Asociando '{producto.nombre}' con la categoría '{categoria.nombre}'...")
            producto.categorias.append(categoria)
            session.add(producto)
            session.commit()
        else:
            print(f"[4/5] El producto '{producto.nombre}' ya está asociado a '{categoria.nombre}'.")

        # 5. Verificación final: Volvemos a consultar para estar seguros
        print("\n--- VERIFICACIÓN ---")
        session.refresh(producto)
        print(f"Producto: {producto.nombre}")
        print(f"Categorías asociadas: {[c.nombre for c in producto.categorias]}")
        
        if any(c.nombre == "Bebidas" for c in producto.categorias):
            print("\n[SUCCESS] ¡ÉXITO! La relación Muchos a Muchos está funcionando correctamente.")
            print("La tabla 'producto_categoria' hizo su trabajo.")
        else:
            print("\n[ERROR] ERROR: La asociación no se guardó correctamente.")

if __name__ == "__main__":
    try:
        probar_muchos_a_muchos()
    except Exception as e:
        print(f"\n[CRITICAL ERROR] ERROR CRITICO: {e}")
        print("\nAsegurate de que PostgreSQL esté corriendo y que la base de datos 'proyecto_programacion' exista.")
