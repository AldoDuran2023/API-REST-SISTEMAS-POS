from flask import Blueprint, request, jsonify,url_for
from models.Compra import Compra
from models.Producto import Producto
from utils.paginador import paginar_query
from funtion_jwt import validate_token
from utils.db import db
from utils.auth_middleware import role_required

compras = Blueprint('compras', __name__)

@compras.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

# Obtener las compras por paginacion
@compras.route('/', methods=['GET'])
@role_required(["admin"])  
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    campos = ['id', 'proveedor_id', 'fecha_compra', 'subtotal', 'igv', 'total', 'estado']
    
    # Obtener la consulta base
    query = Compra.query
    result = paginar_query(query, page, per_page, 'compras.get_categorias_paginated', fields=campos)

    return jsonify(result), 200

# crear una nueva compra
@compras.route('/add', methods=['POST'])
@role_required(["admin"])  
def add_compra():
    data = request.json
    
    proveedor_id = data.get('proveedor_id')
    fecha_compra = data.get('fecha_compra')
    estado = data.get('estado', "En camino")
    
    try:
        new_compra = Compra(proveedor_id=proveedor_id, fecha_compra=fecha_compra, estado=estado)
        
        # Agregar detalles de compra
        for detalle_data in data.get('detalles', []):
            detalle = DetalleCompra(
                producto_id=detalle_data['producto_id'],
                cantidad=detalle_data['cantidad'],
                precio_compra=detalle_data['precio_compra']
            )
            new_compra.add_detalle(detalle)
        
        db.session.add(new_compra)
        db.session.commit()
        return jsonify({
            'message': 'Compra registrada con éxito',
            'data': {
                'id': new_compra.id,
                'proveedor_id': new_compra.proveedor_id,
                'fecha_compra': new_compra.fecha_compra,
                'subtotal': new_compra.subtotal,
                'igv': new_compra.igv,
                'total': new_compra.total,
                'estado': new_compra.estado
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': 'Error al registrar la compra'}), 500
    
# seleccionar una compra
@compras.route('/<int:id>', methods=['GET'])
@role_required(["admin"])  
def get_compra(id):
    compra = Compra.query.get_or_404(id)
    try:
        compra_data = {
            'id': compra.id,
            'proveedor_id': compra.proveedor_id,
            'fecha_compra': compra.fecha_compra,
            'subtotal': compra.subtotal,
            'igv': compra.igv,
            'total': compra.total,
            'estado': compra.estado
        }
        return jsonify({
            'message': 'Compra seleccionada correctamente',
            'data': compra_data
        }), 200
    except Exception as e:
        return jsonify({'message': 'compra no encontrada'}), 500
    
# Actualizar una compra
@compras.route('/update/<int:id>', methods=['PUT'])
@role_required(["admin"])  
def update_compra(id):
    compra = Compra.query.get_or_404(id)
    compra_data = request.json

    try:
        # Verificar si el estado cambió a "Recibido"
        estado_anterior = compra.estado
        nuevo_estado = compra_data['estado']

        compra.estado = nuevo_estado

        # Si la compra se marca como "Recibido", actualizar el stock de los productos
        if estado_anterior != "Recibido" and nuevo_estado == "Recibido":
            for detalle in compra.detalles:
                producto = Producto.query.get(detalle.producto_id)
                if producto:
                    producto.stock += detalle.cantidad  # Sumar al stock actual

        db.session.commit()
        return jsonify({'message': 'Compra editada correctamente y stock actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': 'Error al actualizar la compra'}), 500
    
# Eliminar una Compra
@compras.route('/delete/<int:id>', methods=['DELETE'])
@role_required(["admin"])  
def delete_compra(id):
    compra = Compra.query.get_or_404(id)
    try:
        db.session.delete(compra)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': 'Error al eliminar la compra'})