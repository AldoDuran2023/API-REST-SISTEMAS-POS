from utils.db import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compra'
    
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    fecha_compra = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    subtotal = db.Column(db.Float, nullable=False, default=0)
    igv = db.Column(db.Float, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False, default=0)
    estado = db.Column(db.Enum("Recibido", "En camino"), nullable=False, default="En camino")
    
    proveedor = db.relationship("Proveedor", back_populates="compras")
    detalles = relationship("DetalleCompra", back_populates="compra", cascade="all, delete-orphan")

    def __init__(self, proveedor_id=None, fecha_compra=None, estado="En camino"):
        self.proveedor_id = proveedor_id
        self.fecha_compra = fecha_compra
        self.estado = estado
