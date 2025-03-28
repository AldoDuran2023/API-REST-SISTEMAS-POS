from utils.db import db
from models.Producto import Producto
from sqlalchemy.orm import relationship

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False, default=0)
    subtotal = db.Column(db.Float, nullable=False, default=0)
    
    producto = relationship("Producto", back_populates="detalles_venta")
    venta = relationship("Venta", back_populates="detalles")
    
    def __init__(self, producto_id=None, venta_id=None, cantidad=0):
        self.producto_id = producto_id
        self.venta_id = venta_id
        self.cantidad = cantidad
        self.set_precio_unitario()
        self.calculate_subtotal()
        
    def set_precio_unitario(self):
        producto = Producto.query.get(self.producto_id)
        if producto:
            self.precio_unitario = producto.precio_venta  
        else:
            self.precio_unitario = 0
        
    def calculate_subtotal(self):
        self.subtotal = self.cantidad * self.precio_unitario
