from utils.db import db
from sqlalchemy.orm import relationship

class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'
    
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_compra = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False, default=0)

    compra = db.relationship("Compra", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles")
    
    def __init__(self, compra_id=None, producto_id=None, cantidad=0, precio_compra=0):
        self.compra_id = compra_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.calculate_subtotal()

    def calculate_subtotal(self):
        """Calcula el subtotal basado en la cantidad y el precio de compra."""
        self.subtotal = self.cantidad * self.precio_compra
