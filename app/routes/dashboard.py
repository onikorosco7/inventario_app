from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.models.producto import Producto

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    total_productos = db.query(Producto).count()
    productos_bajo_stock = db.query(Producto).filter(Producto.stock < Producto.stock_minimo).count()
    productos_agotados = db.query(Producto).filter(Producto.stock == 0).count()

    return {
        "total_productos": total_productos,
        "productos_bajo_stock": productos_bajo_stock,
        "productos_agotados": productos_agotados
    }