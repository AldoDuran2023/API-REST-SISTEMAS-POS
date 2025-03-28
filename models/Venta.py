from utils.db import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Venta(db.Model):
    __tablename__ = 'venta'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    subtotal = db.Column(db.Float, nullable=False, default=0)
    igv = db.Column(db.Float, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False, default=0)
    metodo_pago = db.Column(db.Enum("efectivo", "yape", "plin"), nullable=False, default="efectivo")
    
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    
    def __init__(self, fecha=None, subtotal=0, igv=0, total=0, metodo_pago="efectivo"):
        self.fecha = fecha
        self.subtotal = subtotal
        self.igv = igv
        self.total = total
        self.metodo_pago = metodo_pago
        
    