from utils.db import db

class Marca(db.Model):
    __tablename__ = 'marca'

    id = db.Column(db.Integer, primary_key=True)  
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    
    # Relacion con la clase Productos
    productos = db.relationship('Producto', back_populates='marca', cascade="all, delete-orphan")
    
    def __init__(self, nombre):
        self.nombre = nombre