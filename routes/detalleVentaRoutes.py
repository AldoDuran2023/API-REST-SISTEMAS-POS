from flask import Blueprint, request, jsonify
from utils.db import db
from models.Venta import Venta
from models.DetalleVenta import DetalleVenta
from models.Producto import Producto
from funtion_jwt import validate_token
from utils.paginador import paginar_query
from routes.ventaRoute import actualizar_totales_venta

detalle_venta = Blueprint('detalle_venta', __name__)

@detalle_venta.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

def actualizar_stock_producto(producto_id, cantidad, operacion='disminuir'):
    producto = Producto.query.get(producto_id)
    if not producto:
        raise ValueError(f'Producto con ID {producto_id} no existe')
    
    if operacion == 'disminuir':
        if producto.stock < cantidad:
            raise ValueError(f'Stock insuficiente para el producto {producto_id}')
        producto.stock -= cantidad
    elif operacion == 'aumentar':
        producto.stock += cantidad
    
    db.session.commit()

@detalle_venta.route('/', methods=['GET'])
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    campos = ['id', 'venta_id', 'producto_id', 'cantidad', 'precio_unitario', 'subtotal']
    query = DetalleVenta.query
    result = paginar_query(query, page, per_page, 'detalle_venta.get_categorias_paginated', fields=campos)
    return jsonify(result), 200

@detalle_venta.route('/add', methods=['POST'])
def add_detalle_venta():
    data = request.json
    
    venta_id = data.get('venta_id')
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    
    try:
        # Verificar si la venta existe
        venta = Venta.query.get(venta_id)
        if not venta:
            return jsonify({'message': f'Venta con ID {venta_id} no existe'}), 400
        
        # Verificar si el producto existe
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({'message': f'Producto con ID {producto_id} no existe'}), 400
        
        # Actualizar stock del producto
        actualizar_stock_producto(producto_id, cantidad, 'disminuir')
        
        # Buscar si el producto ya está en la venta
        detalle_existente = DetalleVenta.query.filter_by(
            venta_id=venta_id, 
            producto_id=producto_id
        ).first()
        
        if detalle_existente:
            # Si el producto ya está, actualizar cantidad
            detalle_existente.cantidad += cantidad
            detalle_existente.calculate_subtotal()
        else:
            # Crear nuevo detalle de venta
            nuevo_detalle = DetalleVenta(
                producto_id=producto_id,
                venta_id=venta_id,
                cantidad=cantidad
            )
            db.session.add(nuevo_detalle)
        
        db.session.commit()
        
        # Actualizar totales de la venta
        actualizar_totales_venta(venta_id)
        
        return jsonify({'message': 'Detalle de venta agregado correctamente'}), 200
    
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al agregar detalle de venta', 'error': str(e)}), 500

@detalle_venta.route('/<int:venta_id>', methods=['GET'])
def listar_detalles_venta(venta_id):
    try:
        # Verificar si la venta existe
        venta = Venta.query.get_or_404(venta_id)
        
        # Obtener detalles de la venta
        detalles = DetalleVenta.query.filter_by(venta_id=venta_id).all()
        
        resultado = [{
            'id': detalle.id,
            'producto_id': detalle.producto_id,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.precio_unitario,
            'subtotal': detalle.subtotal
        } for detalle in detalles]
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'message': 'Error al listar detalles de venta', 'error': str(e)}), 500

@detalle_venta.route('/update/<int:detalle_id>', methods=['PUT'])
def editar_detalle_venta(detalle_id):
    data = request.json
    
    try:
        # Buscar el detalle de venta
        detalle = DetalleVenta.query.get_or_404(detalle_id)
        
        # Calcular diferencia de cantidad
        cantidad_nueva = data.get('cantidad')
        if cantidad_nueva is not None:
            if cantidad_nueva > detalle.cantidad:
                # Aumentar cantidad, disminuir stock
                diferencia = cantidad_nueva - detalle.cantidad
                actualizar_stock_producto(detalle.producto_id, diferencia, 'disminuir')
            elif cantidad_nueva < detalle.cantidad:
                # Disminuir cantidad, aumentar stock
                diferencia = detalle.cantidad - cantidad_nueva
                actualizar_stock_producto(detalle.producto_id, diferencia, 'aumentar')
            
            detalle.cantidad = cantidad_nueva
        
        # Recalcular subtotal
        detalle.calculate_subtotal()
        
        db.session.commit()
        
        # Actualizar totales de la venta
        actualizar_totales_venta(detalle.venta_id)
        
        return jsonify({'message': 'Detalle de venta actualizado correctamente'}), 200
    
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al editar detalle de venta', 'error': str(e)}), 500

@detalle_venta.route('/delete/<int:detalle_id>', methods=['DELETE'])
def eliminar_detalle_venta(detalle_id):
    try:
        # Buscar el detalle de venta
        detalle = DetalleVenta.query.get_or_404(detalle_id)
        
        # Guardar la venta_id y producto_id antes de eliminar
        venta_id = detalle.venta_id
        producto_id = detalle.producto_id
        cantidad = detalle.cantidad
        
        # Aumentar stock del producto
        actualizar_stock_producto(producto_id, cantidad, 'aumentar')
        
        # Eliminar detalle
        db.session.delete(detalle)
        db.session.commit()
        
        # Actualizar totales de la venta
        actualizar_totales_venta(venta_id)
        
        return jsonify({'message': 'Detalle de venta eliminado correctamente'}), 200
    
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar detalle de venta', 'error': str(e)}), 500