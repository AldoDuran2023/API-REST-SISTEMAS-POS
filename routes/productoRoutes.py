from flask import Blueprint, request, jsonify,url_for
from models.Producto import Producto
from utils.paginador import paginar_query
from funtion_jwt import validate_token
from utils.db import db

productos = Blueprint('productos', __name__)

@productos.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

@productos.route('/', methods=['GET'])
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    campos = ['id', 'nombre', 'descripcion', 'categoria_id', 'marca_id', 'precio_compra', 'precio_venta', 'stock', 'stock_minimo', 'imagen', 'utilidad']
    # Obtener la consulta base
    query = Producto.query
    result = paginar_query(query, page, per_page, 'productos.get_categorias_paginated', fields=campos)

    return jsonify(result), 200

# Ruta para agregar un nuevo producto
@productos.route('/add', methods=['POST'])
def add_producto():
    data = request.json

    nombre = data.get('nombre')
    descripcion = data.get('descripcion', None)
    categoria_id = data.get('categoria_id', None)
    marca_id = data.get('marca_id', None)
    precio_compra = data.get('precio_compra', 0)
    precio_venta = data.get('precio_venta', 0)
    stock = data.get('stock', 0)
    stock_minimo = data.get('stock_minimo', 10)
    imagen = data.get('imagen', "default.png")

    try:
        new_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            categoria_id=categoria_id,
            marca_id=marca_id,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            stock_minimo=stock_minimo,
            imagen=imagen
        )

        db.session.add(new_producto)
        db.session.commit()

        return jsonify({
            'message': 'Producto agregado con éxito',
            'data': {
                'id': new_producto.id,
                'nombre': new_producto.nombre,
                'descripcion': new_producto.descripcion,
                'categoria_id': new_producto.categoria_id,
                'marca_id': new_producto.marca_id,
                'precio_compra': new_producto.precio_compra,
                'precio_venta': new_producto.precio_venta,
                'stock': new_producto.stock,
                'stock_minimo': new_producto.stock_minimo,
                'imagen': new_producto.imagen,
                'utilidad': new_producto.utilidad 
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Seleccionar un producto
@productos.route('/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get_or_404(id)
    producto_data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'categoria_id': producto.categoria_id,
        'marca_id': producto.marca_id,
        'precio_compra': producto.precio_compra,
        'precio_venta': producto.precio_venta,
        'stock': producto.stock,
        'stock_minimo': producto.stock_minimo,
        'imagen': producto.imagen,
        'utilidad': producto.utilidad 
    }
    return jsonify({
        'message': 'Producto seleccionado correctamente',
        'data': producto_data
    }), 200
    
# Actualizar un producto
@productos.route('/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get_or_404(id)
    producto_data = request.json
    
    try:
        producto.nombre = producto_data['nombre']
        producto.descripcion = producto_data['descripcion']
        producto.categoria_id = producto_data['categoria_id']
        producto.marca_id = producto_data['marca_id']
        producto.precio_compra = producto_data['precio_compra']
        producto.precio_venta = producto_data['precio_venta']
        producto.stock = producto_data['stock']
        producto.stock_minimo = producto_data['stock_minimo']
        producto.imagen = producto_data['imagen']

        db.session.commit()
        
        return jsonify({
            'message': 'Producto actualizado exitosamente',
            'utilidad': producto.utilidad
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error al actualizar el producto',
            'error': str(e)
        }), 400
    
# Eliminar producto
@productos.route('/delete/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    
    try:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': 'Producto eliminada correctamente'})
    except Exception as e:
        bd.session.rollback()
        return jsonify({'message': 'Error al eliminar el producto'}), 500