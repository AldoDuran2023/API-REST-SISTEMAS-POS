from utils.db import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Cambiado a String
    estado = db.Column(db.Enum("activo", "inactivo"), default="activo")
    rol = db.Column(db.Enum("admin", "empleado"))
    
    def __init__(self, nombre=None, email=None, password=None, estado="activo", rol="empleado"):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.estado = estado
        self.rol = rol