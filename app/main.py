from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os

from app.database.conexion import engine, Base, get_db
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.routes import producto, auth

# Iniciamos la aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory=os.path.join("app", "templates"))

# Crear tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

# Rutas estáticas
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CORS (habilitado para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas incluidas
app.include_router(producto.router)
app.include_router(auth.router)

# Ruta principal
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "titulo": "Bienvenido a OnikStore"})

# Nueva ruta para ver productos
@app.get("/productos", response_class=HTMLResponse)
def ver_productos(request: Request, db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return templates.TemplateResponse("productos.html", {"request": request, "productos": productos})

# Ruta de prueba
@app.get("/api")
def read_root():
    return {"message": "Bienvenido al sistema de gestión de inventario de OnikStore"}
