from flask import Blueprint, request, jsonify
from models.DetalleCompra import DetalleCompra
from models.Producto import Producto
from models.Compra import Compra
from funtion_jwt import validate_token
from utils.paginador import paginar_query
from utils.db import db
from utils.auth_middleware import role_required

detalle_compra = Blueprint('detalle_compra', __name__)

@detalle_compra.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

def actualizar_totales_compra(compra_id):
    """ Recalcula el subtotal, IGV y total de la compra """
    compra = Compra.query.get(compra_id)
    if not compra:
        return False
    
    # Calcular nuevo subtotal sumando los subtotales de los detalles de compra
    compra.subtotal = sum(detalle.subtotal for detalle in compra.detalles)
    
    # Calcular el IGV (18%)
    compra.igv = round(compra.subtotal * 0.18, 2)

    # Calcular el total
    compra.total = round(compra.subtotal + compra.igv, 2)

    db.session.commit()
    return True

@detalle_compra.route('/', methods=['GET'])
@role_required(["admin"])  
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    campos = ['id', 'compra_id', 'producto_id', 'cantidad', 'precio_compra', 'subtotal']
    query = DetalleCompra.query
    result = paginar_query(query, page, per_page, 'compras.get_categorias_paginated', fields=campos)
    return jsonify(result), 200

# Agregar un nuevo detalle de compra
@detalle_compra.route('/add', methods=['POST'])
@role_required(["admin"])  
def add_detalle_compra():
    data = request.json
    
    compra_id = data.get('compra_id')
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    precio_compra = data.get('precio_compra')
    
    # Verificar si el producto y la compra existen
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'message': f'Error: No existe el producto con ID {producto_id}'}), 400
    
    compra = Compra.query.get(compra_id)
    if not compra:
        return jsonify({'message': f'Error: No existe la compra con ID {compra_id}'}), 400

    try:
        # Buscar si el producto ya está en la compra
        detalle_existente = DetalleCompra.query.filter_by(compra_id=compra_id, producto_id=producto_id).first()

        if detalle_existente:
            # Si el producto ya está en la compra, solo actualizar la cantidad
            detalle_existente.cantidad += cantidad
            db.session.commit()
        else:
            # Si no existe, crear un nuevo detalle
            new_detalle_compra = DetalleCompra(
                compra_id=compra_id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_compra=precio_compra
            )
            db.session.add(new_detalle_compra)
            db.session.commit()
        
        actualizar_totales_compra(compra_id)

        return jsonify({'message': 'Detalle de compra actualizado correctamente'}), 200

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': 'Error al registrar el producto'}), 500


# Actualizar el detalle detalle de compra
@detalle_compra.route('/update/<int:id>', methods=['PUT'])
@role_required(["admin"])  
def update_detalle_compra(id):
    data = request.json
    detalle = DetalleCompra.query.get_or_404(id)
    try:
        detalle.cantidad = data['cantidad']
        detalle.precio_compra = data['precio_compra']
        detalle.producto_id = data['producto_id']
        db.session.commit()
        actualizar_totales_compra(compra_id)
        return jsonify({'message': 'Detalle de compra actualizado correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar el detalle de la compra', 'error': str(e)}), 500

# Eliminar un detella compra
@detalle_compra.route('/delete/<int:id>', methods=['DELETE'])
@role_required(["admin"])  
def delete_detalle_compra(id):
    detalle = DetalleCompra.query.get_or_404(id)
    try:
        compra_id = detalle.compra_id
        db.session.delete(detalle)
        db.session.commit()
        actualizar_totales_compra(compra_id)
        return jsonify({'message': 'Producto quitado de la compra'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar el detalle de la compra', 'error': str(e)}), 500