-- Crear las base de datos
CREATE DATABASE inventario_db;
USE inventario_db;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(100) NOT NULL
);
DROP TABLE IF EXISTS usuarios;
-- Tabla categorias
CREATE TABLE categorias  (
id INT auto_increment primary key,
nombre varchar(100) not null,
descripcion text
);

-- Tabla productos 
CREATE TABLE productos (
id INT auto_increment primary key,
nombre varchar(150) not null,
descripcion text,
precio decimal(10,2) not null,
stock int not null,
stock_minimo int default 5,
categoria_id int,
fecha_registro datetime default current_timestamp,
foreign key (categoria_id) references categorias(id)
);


-- Datos de ejemplo
insert into categorias (nombre, descripcion) values
('Bebidas','Productos líquidos para consumo'),
('Snacks', 'Productos para picar'),
('Abarrotes', 'Productos básicos de supermercado'),
('Carnes', 'Cortes de carne fresca'),
('Panadería', 'Productos horneados y panes frescos'),
('Limpieza', 'Productos para higiene y limpieza del hogar'),
('Electrodomésticos', 'Productos electrónicos para el hogar'),
('Ropa', 'Prendas de vestir para todas las edades');


insert into productos (nombre, descripcion, precio, stock, stock_minimo, categoria_id) values
('Agua mineral 600ml', 'Agua sin gas', 2.50, 20, 5, 1),
('Galletas de avena', 'Paquete de 6 unidades', 3.00, 10, 3, 2),
('Arroz 1kg', 'Arroz de grano largo', 1.80, 50, 10, 1),
('Carne molida 500g', 'Carne de res molida', 5.50, 30, 7, 2),
('Pan de molde', 'Paquete de pan de 10 rebanadas', 2.20, 40, 8, 3),
('Detergente líquido', 'Botella de detergente de 1L', 3.80, 15, 5, 4),
('Refrigeradora', 'Refrigeradora de 350L', 1200.00, 5, 1, 5),
('Camiseta algodón', 'Camiseta básica de algodón talla M', 8.00, 60, 15, 6);

DELETE FROM productos;

ALTER TABLE productos CHANGE stock_minino stock_minimo DECIMAL(10,2) NOT NULL;
