from sqlmodel import SQLModel, Field

import sqlalchemy as sa


class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    producto_id: int = Field(
        sa_column=sa.Column(
            sa.BigInteger,
            sa.ForeignKey("producto.id"),
            primary_key=True,
        )
    )

    ingrediente_id: int = Field(
        sa_column=sa.Column(
            sa.BigInteger,
            sa.ForeignKey("ingrediente.id"),
            primary_key=True,
        )
    )

    # ---- Atributos ----

    es_removible: bool = Field(default=False)

    # ---- Audit ---- no hay
