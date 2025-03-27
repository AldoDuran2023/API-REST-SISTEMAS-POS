from utils.db import db

class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    
    # Relacion con la clase productos
    productos = db.relationship('Producto', back_populates='categoria', cascade="all, delete-orphan") 
    
    def __init__(self, nombre):
        self.nombre = nombre