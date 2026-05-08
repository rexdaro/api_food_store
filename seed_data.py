# Seeding script for food store
import sys
import os

# Add the current directory to sys.path to allow importing 'app'
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.db.database import engine
from app.modules.productos.models import Producto, ProductoCategoria, ProductoIngrediente
from app.modules.categorias.models import Categoria
from app.modules.ingredientes.models import Ingrediente
import random

def seed():
    with Session(engine) as session:
        # 1. Ingredients
        ingredientes_data = [
            ("Pan de Brioche", "Pan tierno y mantecoso", False),
            ("Carne de Res", "180g de carne seleccionada", False),
            ("Queso Cheddar", "Fetas de cheddar real", False),
            ("Bacon", "Panceta ahumada crocante", False),
            ("Cebolla Caramelizada", "Cebolla dulce a fuego lento", False),
            ("Lechuga Fresca", "Lechuga hidropónica", False),
            ("Tomate", "Tomate perita en rodajas", False),
            ("Pepinillos", "Pepinillos agridulces", False),
            ("Huevo Frito", "Huevo de campo", False),
            ("Harina 000", "Base para pizzas y pastas", False),
            ("Salsa de Tomate", "Receta de la casa", False),
            ("Mozzarella", "Queso hilado de alta calidad", False),
            ("Aceitunas Negras", "Aceitunas griegas", False),
            ("Aceitunas Verdes", "Aceitunas rellenas", False),
            ("Pimentón", "Especias dulces", False),
            ("Orégano", "Hierba aromática seca", False),
            ("Papas", "Papas blancas para freír", False),
            ("Salitre", "Conservante natural", True), # Allergen example
            ("Maní", "Frutos secos", True), # Allergen
            ("Gluten", "Presente en harinas", True), # Allergen
        ]
        
        db_ingredients = []
        for nombre, desc, alergeno in ingredientes_data:
            ing = session.exec(select(Ingrediente).where(Ingrediente.nombre == nombre)).first()
            if not ing:
                ing = Ingrediente(nombre=nombre, descripcion=desc, es_alergeno=alergeno)
                session.add(ing)
            db_ingredients.append(ing)
        session.commit()
        for ing in db_ingredients:
            session.refresh(ing)
            
        # 2. Categories
        categorias_data = [
            "Hamburguesas", "Pizzas", "Bebidas", "Postres", "Ensaladas", 
            "Entradas", "Cafetería", "Cervezas Artesanales", "Pastas", "Minutas"
        ]
        
        db_categories = []
        for nombre in categorias_data:
            cat = session.exec(select(Categoria).where(Categoria.nombre == nombre)).first()
            if not cat:
                cat = Categoria(nombre=nombre, descripcion=f"Variedad de {nombre.lower()}")
                session.add(cat)
            db_categories.append(cat)
        session.commit()
        for cat in db_categories:
            session.refresh(cat)

        # 3. Products (30)
        productos_data = [
            # Hamburguesas
            ("Doble Cheeseburger", "Dos carnes, doble cheddar, cebolla y pepinillos", 4500, 50, ["https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500"]),
            ("Bacon Burger", "Carne, cheddar, bacon crocante y barbacoa", 5200, 30, ["https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500"]),
            ("Onion Burger", "Carne, cheddar y mucha cebolla caramelizada", 4800, 25, ["https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=500"]),
            ("Veggie Delight", "Medallón de lentejas, lechuga, tomate y palta", 4200, 20, ["https://images.unsplash.com/photo-1512152272829-e3139592d56f?w=500"]),
            ("Fried Egg Burger", "Carne, queso, huevo frito y lechuga", 4900, 15, ["https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500"]),
            
            # Pizzas
            ("Muzzarella", "Salsa de tomate, muzzarella y aceitunas", 6500, 40, ["https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500"]),
            ("Napolitana", "Muzzarella, rodajas de tomate y ajo", 7200, 30, ["https://images.unsplash.com/photo-1574071318508-1cdbad80ad50?w=500"]),
            ("Fugazzetta", "Mucha cebolla, muzzarella y especias", 7500, 20, ["https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=500"]),
            ("Pepperoni", "Salsa de tomate, muzzarella y pepperoni", 8000, 25, ["https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500"]),
            ("Especial", "Muzzarella, jamón, morrones y huevo", 8500, 15, ["https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?w=500"]),

            # Bebidas
            ("Coca Cola 500ml", "Refresco clásico", 1200, 100, ["https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500"]),
            ("Agua Mineral", "Con o sin gas", 1000, 200, ["https://images.unsplash.com/photo-1548839140-29a74f847f4b?w=500"]),
            ("Limonada", "Limón natural con menta y jengibre", 1500, 50, ["https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"]),
            ("Sprite 500ml", "Refresco de lima-limón", 1200, 80, ["https://images.unsplash.com/photo-1625772290748-3912a304ef76?w=500"]),

            # Cervezas
            ("IPA Artesanal", "Intenso aroma cítrico y amargor equilibrado", 2500, 60, ["https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=500"]),
            ("Honey Beer", "Suave con un toque de miel", 2400, 45, ["https://images.unsplash.com/photo-1584225064785-c62a8b43d148?w=500"]),
            ("Stout Negra", "Notas de café y chocolate", 2600, 35, ["https://images.unsplash.com/photo-1618883635542-c518f0814675?w=500"]),

            # Minutas
            ("Milanesa con Papas", "Carne de ternera con guarnición", 5500, 40, ["https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500"]),
            ("Suprema Napolitana", "Pollo con muzzarella y tomate", 6200, 30, ["https://images.unsplash.com/photo-1632778149975-420e0e75ee08?w=500"]),
            ("Papas con Cheddar", "Porción para compartir", 3500, 50, ["https://images.unsplash.com/photo-1573016608464-5bb71db060e2?w=500"]),

            # Pastas
            ("Ravioles de Espinaca", "Con salsa bolognesa", 5800, 25, ["https://images.unsplash.com/photo-1473093226795-af9932fe5856?w=500"]),
            ("Fideos al Pesto", "Pasta fresca con pesto casero", 4500, 30, ["https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=500"]),
            ("Ñoquis del 29", "Tradicionales con tuco", 4800, 20, ["https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=500"]),

            # Postres
            ("Chocotorta", "Clásico postre argentino", 2200, 20, ["https://images.unsplash.com/photo-1606312619070-d48b4c652a52?w=500"]),
            ("Flan con Dulce", "Flan casero", 1800, 25, ["https://images.unsplash.com/photo-1528975604071-b4dc52a2d18c?w=500"]),
            ("Tiramisú", "Café y mascarpone", 2500, 15, ["https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500"]),

            # Entradas
            ("Bastones de Muzzarella", "6 unidades con salsa", 2800, 40, ["https://images.unsplash.com/photo-1531390554824-30799b0ba84a?w=500"]),
            ("Nachos con Queso", "Crocantes con dip de queso", 2600, 35, ["https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?w=500"]),
            ("Empanadas (Docena)", "Carne, jamón y queso, choclo", 7500, 20, ["https://images.unsplash.com/photo-1552332386-f8dd00dc2f85?w=500"]),
            ("Rabas", "Aros de calamar fritos", 6000, 15, ["https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500"]),
        ]

        for nombre, desc, precio, stock, imgs in productos_data:
            prod = session.exec(select(Producto).where(Producto.nombre == nombre)).first()
            if not prod:
                prod = Producto(
                    nombre=nombre, 
                    descripcion=desc, 
                    precio_base=precio, 
                    stock_cantidad=stock, 
                    imagenes_url=imgs,
                    disponible=True
                )
                session.add(prod)
                session.commit()
                session.refresh(prod)
                
                # Assign to category
                cat_name = ""
                if any(x in nombre for x in ["Burger", "Cheeseburger", "Veggie"]): cat_name = "Hamburguesas"
                elif any(p in nombre for p in ["Pizza", "Muzzarella", "Napolitana", "Fugazzetta", "Pepperoni", "Especial"]): cat_name = "Pizzas"
                elif any(b in nombre for b in ["Coca", "Agua", "Limonada", "Sprite"]): cat_name = "Bebidas"
                elif any(p in nombre for p in ["Chocotorta", "Flan", "Tiramisú"]): cat_name = "Postres"
                elif any(m in nombre for m in ["Milanesa", "Suprema", "Papas con Cheddar"]): cat_name = "Minutas"
                elif any(p in nombre for p in ["Ravioles", "Fideos", "Ñoquis"]): cat_name = "Pastas"
                elif any(c in nombre for c in ["IPA", "Honey", "Stout"]): cat_name = "Cervezas Artesanales"
                elif any(e in nombre for e in ["Bastones", "Nachos", "Empanadas", "Rabas"]): cat_name = "Entradas"
                
                if cat_name:
                    cat = session.exec(select(Categoria).where(Categoria.nombre == cat_name)).first()
                    if cat:
                        link = ProductoCategoria(producto_id=prod.id, categoria_id=cat.id)
                        session.add(link)
                
                # Assign random ingredients
                num_ing = random.randint(2, 5)
                selected_ing = random.sample(db_ingredients, num_ing)
                for ing in selected_ing:
                    link = ProductoIngrediente(producto_id=prod.id, ingrediente_id=ing.id)
                    session.add(link)
        
        session.commit()
        print("Successfully seeded 30 products, 10 categories, and various ingredients!")

if __name__ == "__main__":
    seed()
