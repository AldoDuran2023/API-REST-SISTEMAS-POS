from flask import Blueprint, jsonify, request, url_for
from models.Categoria import Categoria
from funtion_jwt import validate_token
from utils.db import db
from utils.paginador import paginar_query
from utils.auth_middleware import role_required

categorias = Blueprint('categorias', __name__)

# solo los usuarios autentificados pueda acceder
@categorias.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)
    # si sale todo bien continua pero si hay un error

@categorias.route('/', methods=['GET'])
@role_required(["admin"])  
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    # Obtener la consulta base
    query = Categoria.query
    result = paginar_query(query, page, per_page, 'categorias.get_categorias_paginated', fields=['id', 'nombre'])

    return jsonify(result), 200



# Añadir una nueva categoria
@categorias.route('/add', methods=['POST'])
@role_required(["admin"])  
def add_categoria():
    data = request.json
    nombre = data.get('nombre')
    
    try:
        new_categoria = Categoria(nombre)
        db.session.add(new_categoria)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    return jsonify({
            'message': 'Categoria Agregada con éxito',
            'data': {
                'id': new_categoria.id,
                'nombre': new_categoria.nombre
            }
        }), 201
    
# Seleccionar una categoria
@categorias.route('/<int:id>', methods=['GET'])
@role_required(["admin"])  
def get_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    categoria_data = {
        'id': categoria.id,
        'nombre': categoria.nombre
    }
    return jsonify({
        'message': 'Categoria seleccionado correctamente',
        'data': categoria_data
    }), 200
    
@categorias.route('/<int:id>', methods=['PUT'])
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    data = request.json
    
    try:
        categoria.nombre = data['nombre']
        db.session.commit()  
    except Exception as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'message': 'Categoría editada con éxito',
        'data': {
            'id': categoria.id,  
            'nombre': categoria.nombre
        }
    }), 200  # Código 200 es más apropiado para actualizaciones exitosas

    
# eliminar una Categoria
@categorias.route('/<int:id>', methods=['DELETE'])
@role_required(["admin"])  
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    
    return jsonify({'message': 'Categoria eliminada correctamente'})