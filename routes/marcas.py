from flask import Blueprint, request, jsonify, url_for
from models.Marca import Marca
from utils.db import db
from funtion_jwt import validate_token
from utils.paginador import paginar_query
from utils.auth_middleware import role_required

marcas = Blueprint('marcas', __name__)

# solo los usuarios autentificados pueda acceder
@marcas.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)
    # si sale todo bien continua pero si hay un error

@marcas.route('/', methods=['GET'])
@role_required(["admin"]) 
def get_marcas_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    # Obtener la query base
    query = Marca.query

    # Aplicar la paginación usando la función reutilizable
    result = paginar_query(query, page, per_page, 'marcas.get_marcas_paginated', fields=['id', 'nombre'])

    return jsonify(result), 200

# obtener marca
@marcas.route('/<int:id>', methods=['GET'])
@role_required(["admin"]) 
def get_marca(id):
    marca = Marca.query.get_or_404(id)
    marca_data = {
        'id': marca.id,
        'nombre': marca.nombre
    }
    return jsonify({
        'message': 'Marca seleccionada correctamente',
        'data': marca_data
    }), 200

# crear marca
@marcas.route('/new', methods=['POST'])
@role_required(["admin"]) 
def add_marca():
    data = request.json
    nombre = data.get('nombre')
        
    try:
        new_marca = Marca(nombre)
        db.session.add(new_marca)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 500        

    return jsonify({
        'id': new_marca.id,
        'nombre': new_marca.nombre
    }), 201
    
# actualziar una marca
@marcas.route('/<int:id>', methods=['PUT'])
@role_required(["admin"]) 
def update_marca(id):
    marca = Marca.query.get_or_404(id)
    data = request.json
    
    try:
        marca.nombre = data['nombre']
        db.session.commit()  
    except Exception as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 500
        
    db.session.commit()
    
    marca_update = {
        'id': marca.id,
        'nombre': marca.nombre
    }
    
    return jsonify({
        'mesagge': 'Marca Editada con exito',
        'data': marca_update
    }), 201
    
# eliminar marca
@marcas.route('/<int:id>', methods=['DELETE'])
@role_required(["admin"]) 
def delete_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    
    return jsonify({'message': 'Marca eliminada correctamente'})