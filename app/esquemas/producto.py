# app/esquemas/producto.py

from pydantic import BaseModel
from typing import Optional

# Para crear producto
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    stock_minimo: int
    categoria_id: int

# Para actualizar producto
class ProductoUpdate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    stock_minimo: int
    categoria_id: int

# Para retornar producto (con ID incluido)
class ProductoResponse(ProductoCreate):
    id: int

    class Config:
        from_attributes = True  # Usamos esto en vez de orm_mode para Pydantic v2
