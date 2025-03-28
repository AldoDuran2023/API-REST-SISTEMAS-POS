from flask import Blueprint, request, jsonify
from funtion_jwt import write_token, validate_token
from models.User import User
from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Buscar usuario en la base de datos
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        token = write_token({"id": user.id, "email": user.email, "rol": user.rol})
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

@routes_auth.route('/verify/token')
def verify():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token requerido"}), 403
    try:
        token = token.split(" ")[1]
        return validate_token(token, output=True)
    except Exception as e:
        return jsonify({"message": "Token inválido", "error": str(e)}), 403

@routes_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol', 'empleado')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "El usuario ya existe"}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(nombre=nombre, email=email, password=hashed_password, rol=rol)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuario creado exitosamente"}), 201