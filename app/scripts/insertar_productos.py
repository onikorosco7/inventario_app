from app.database.conexion import SessionLocal
from app.models.producto import Producto
from app.models.imagen_producto import ImagenProducto

db = SessionLocal()

nuevo_producto = Producto(
    nombre="Helado de fresa",
    precio=4.50,
    descripcion="Refrescante helado artesanal de fresa",
    stock=30,
    imagen_url="img/fresa_principal.jpg"
)

imagenes = [
    ImagenProducto(url="/img/snacks.jpg"),
    ImagenProducto(url="img/fresa2.jpg"),
    ImagenProducto(url="img/fresa3.jpg")
]

nuevo_producto.imagenes.extend(imagenes)

db.add(nuevo_producto)
db.commit()
db.close()
