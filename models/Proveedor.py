from utils.db import db

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(9), nullable=False)
    direccion = db.Column(db.String(200))
    email = db.Column(db.String(100), nullable=False, unique=True)
    estado = db.Column(db.Enum("activo", "inactivo"), default="activo")
    
    compras = db.relationship('Compra', back_populates='proveedor', cascade="all, delete-orphan")
    
    def __init__(self, nombre=None, telefono=None, direccion=None, email=None, estado="activo"):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.estado = estado