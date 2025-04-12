# app/models/imagen_producto.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.conexion import Base

class ImagenProducto(Base):
    __tablename__ = 'imagenes_producto'

    producto_id = Column(Integer, ForeignKey('productos.id'), primary_key=True)
    imagen_id = Column(Integer, ForeignKey('imagenes.id'), primary_key=True)

    producto = relationship('Producto', back_populates='imagenes')
    imagen = relationship('Imagen', back_populates='productos')
