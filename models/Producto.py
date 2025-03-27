from utils.db import db
from sqlalchemy.orm import relationship


class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(200), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    precio_compra = db.Column(db.Float, nullable=False, default=0)
    precio_venta = db.Column(db.Float, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, nullable=False, default=10)
    imagen = db.Column(db.String(200), nullable=True, default="default.png")
    
    categoria = db.relationship('Categoria', back_populates='productos') 
    marca = db.relationship('Marca', back_populates='productos')
    detalles = db.relationship('DetalleCompra', back_populates='producto', cascade='all, delete-orphan')

    @property
    def utilidad(self):
        """ Calcula la utilidad como la diferencia entre precio de venta y precio de compra """
        return self.precio_venta - self.precio_compra

    def __init__(self, nombre, descripcion=None, categoria_id=None, marca_id=None, precio_compra=0, precio_venta=0, stock=0, stock_minimo=10, imagen="default.png"):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria_id = categoria_id
        self.marca_id = marca_id
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.imagen = imagen
