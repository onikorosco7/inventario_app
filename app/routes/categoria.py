# app/routes/categoria.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.models.categoria import Categoria
from app.esquemas.categoria import CategoriaCreate

router = APIRouter()

# Crear una categoría
@router.post("/categorias/", response_model=CategoriaCreate)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Obtener todas las categorías
@router.get("/categorias/", response_model=list[CategoriaCreate])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

# Obtener una categoría por ID
@router.get("/categorias/{categoria_id}", response_model=CategoriaCreate)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Actualizar una categoría
@router.put("/categorias/{categoria_id}", response_model=CategoriaCreate)
def actualizar_categoria(categoria_id: int, categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_categoria.nombre = categoria.nombre
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Eliminar una categoría
@router.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
    return {"message": "Categoría eliminada"}
