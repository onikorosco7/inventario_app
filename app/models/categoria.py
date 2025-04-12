from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.conexion import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    productos = relationship("Producto", back_populates="categoria")
