from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.conexion import get_db, SessionLocal
from app.models.producto import Producto
from app.esquemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Crear producto
@router.post("/productos/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto) 
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Obtener todos los productos con filtros opcionales
@router.get("/productos/", response_model=list[ProductoResponse])
def obtener_productos(
    nombre: str = Query(None),
    categoria_id: int = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Producto)
    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    return query.all()

@router.get("/productos/exportar_pdf")
def exportar_pdf(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()

    doc = SimpleDocTemplate("productos.pdf", pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("Lista de Productos - OnikStore", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    data = [["ID", "Nombre", "Descripción", "Precio", "Stock", "Categoría"]]

    for p in productos:
        categoria = p.categoria.nombre if p.categoria else "Sin categoría"
        data.append([str(p.id), p.nombre, p.descripcion, f"S/ {p.precio:.2f}", str(p.stock), categoria])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    return FileResponse("productos.pdf", media_type="application/pdf", filename="productos.pdf")


# Obtener producto por ID
@router.get("/productos/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Actualizar producto
@router.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for campo, valor in producto.dict().items():
        setattr(db_producto, campo, valor)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# Eliminar producto
@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado correctamente"}

# Contar el total de productos
@router.get("/productos/total", response_model=int)
def contar_productos(db: Session = Depends(get_db)):
    total_productos = db.query(func.count(Producto.id)).scalar()
    return total_productos

@router.get("/productos/total")
def obtener_total_productos(db: Session = Depends(get_db)):
    total = db.query(Producto).count()
    return {"total_productos": total}

@router.get("/productos/alerta_stock")
def alerta_stock_minimo(db: Session = Depends(get_db)):
    productos_alerta = db.query(Producto).filter(Producto.stock < Producto.stock_minimo).all()
    return productos_alerta

@router.get("/productos")
def ver_productos(request: Request):
    # Obtén los productos desde la base de datos
    db = SessionLocal()
    productos = db.query(Producto).all()
    
    # Renderiza la plantilla y pasa los productos a la vista
    return templates.TemplateResponse("productos.html", {"request": request, "productos": productos})