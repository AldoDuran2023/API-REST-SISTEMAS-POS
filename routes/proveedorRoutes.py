from flask import Blueprint, request, jsonify
from models.Proveedor import Proveedor
from utils.paginador import paginar_query
from funtion_jwt import validate_token
from utils.db import db
from utils.auth_middleware import role_required

proveedor = Blueprint('proveedor', __name__)

@proveedor.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

@proveedor.route('/', methods=['GET'])
@role_required(["admin"])  
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    campos = ['id', 'nombre', 'telefono', 'direccion', 'email', 'estado']
    # Obtener la consulta base
    query = Proveedor.query
    result = paginar_query(query, page, per_page, 'proveedor.get_categorias_paginated', fields=campos)

    return jsonify(result), 200

# Crear un nuevo proveedor
@proveedor.route('/add', methods=['POST'])
@role_required(["admin"])  
def add_proveedor():
    data = request.json

    nombre = data.get('nombre')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    email = data.get('email')

    try:
        new_proveedor = Proveedor(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email
        )
        db.session.add(new_proveedor)
        db.session.commit()

        return jsonify({
            'message': 'Proveedor agregado exitosamente',
            'data': {
                'id': new_proveedor.id,
                'nombre': new_proveedor.nombre,
                'telefono': new_proveedor.telefono,
                'direccion': new_proveedor.direccion,
                'email': new_proveedor.email
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al registrar al proveedor: {str(e)}'}), 500

# Obtener un proveedor por ID
@proveedor.route('/<int:id>', methods=['GET'])
@role_required(["admin"])  
def get_proveedor(id):
    try:
        proveedor = Proveedor.query.get_or_404(id)
        if not proveedor:
            return jsonify({'message': 'Proveedor no encontrado'}), 404
        
        proveedor_data = {
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'telefono': proveedor.telefono,
            'direccion': proveedor.direccion,
            'email': proveedor.email
        }

        return jsonify({
            'message': 'Proveedor seleccionado correcatmente',
            'data': proveedor_data    
        }), 200

    except Exception as e:
        return jsonify({'message': f'Error al obtener el proveedor: {str(e)}'}), 500

# Actualizar un proveedor
@proveedor.route('/update/<int:id>', methods=['PUT'])
@role_required(["admin"])  
def update_proveedor(id):
    data = request.json
    try:
        proveedor = Proveedor.query.get_or_404(id)
        if not proveedor:
            return jsonify({'message': 'Proveedor no encontrado'}), 404

        proveedor.nombre = data.get('nombre', proveedor.nombre)
        proveedor.telefono = data.get('telefono', proveedor.telefono)
        proveedor.direccion = data.get('direccion', proveedor.direccion)
        proveedor.email = data.get('email', proveedor.email)

        db.session.commit()

        return jsonify({'message': 'Proveedor actualizado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar el proveedor: {str(e)}'}), 500

# Eliminar un proveedor
@proveedor.route('/delete/<int:id>', methods=['DELETE'])
@role_required(["admin"])  
def delete_proveedor(id):
    try:
        proveedor = Proveedor.query.get_or_404(id)
        if not proveedor:
            return jsonify({'message': 'Proveedor no encontrado'}), 404

        db.session.delete(proveedor)
        db.session.commit()

        return jsonify({'message': 'Proveedor eliminado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar el proveedor: {str(e)}'}), 500
