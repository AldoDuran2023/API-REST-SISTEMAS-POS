from flask import Blueprint, request, jsonify
from utils.db import db
from models.Venta import Venta
from models.DetalleVenta import DetalleVenta
from models.Producto import Producto
from datetime import datetime
from utils.paginador import paginar_query
from funtion_jwt import validate_token


ventas = Blueprint('ventas', __name__)

@ventas.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

def actualizar_totales_venta(venta_id):
    """ Recalcula el subtotal, IGV y total de la venta """
    venta = Venta.query.get(venta_id)
    if not venta:
        return False
    
    # Calcular nuevo total sumando los subtotales de los detalles de venta
    venta.total = sum(detalle.subtotal for detalle in venta.detalles)
    
    # Calcular el subtotal 
    venta.subtotal = round(venta.total / 1.18, 2)

    # Calcular el IGV
    venta.igv = round(venta.total - venta.subtotal, 2)

    db.session.commit()
    return True

@ventas.route('/', methods=['GET'])
def get_categorias_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    campos = ['id', 'fecha', 'subtotal', 'igv', 'total', 'metodo_pago']
    query = Venta.query
    result = paginar_query(query, page, per_page, 'ventas.get_categorias_paginated', fields=campos)
    return jsonify(result), 200


@ventas.route('/add', methods=['POST'])
def add_venta():
    data = request.json
    
    fecha = data.get('fecha', datetime.utcnow())
    metodo_pago = data.get('metodo_pago', 'efectivo')
    
    try:
        new_venta = Venta(fecha=fecha, metodo_pago=metodo_pago)
        
        for detalle_data in data.get('detalles', []):
            producto_id = detalle_data['producto_id']
            cantidad = detalle_data['cantidad']
            
            # Verificar existencia del producto
            producto = Producto.query.get(producto_id)
            if not producto:
                return jsonify({'message': f'Producto con ID {producto_id} no existe'}), 400
            
            # Crear detalle de venta
            detalle = DetalleVenta(
                producto_id=producto_id,
                venta_id=new_venta.id,
                cantidad=cantidad
            )
            new_venta.detalles.append(detalle)
        
        db.session.add(new_venta)
        db.session.commit()
        
        # Actualizar totales de la venta
        actualizar_totales_venta(new_venta.id)
        
        return jsonify({
            'message': 'Venta registrada correctamente', 
            'venta_id': new_venta.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al generar una nueva venta', 'error': str(e)}), 500

@ventas.route('/', methods=['GET'])
def listar_ventas():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        # Paginación de ventas
        ventas_query = Venta.query.order_by(Venta.fecha.desc())
        total_ventas = ventas_query.count()
        
        # Obtener ventas paginadas
        ventas_paginadas = ventas_query.paginate(page=page, per_page=per_page)
        
        # Formatear resultados
        resultado = {
            'total_ventas': total_ventas,
            'pagina_actual': page,
            'total_paginas': ventas_paginadas.pages,
            'ventas': [
                {
                    'id': venta.id,
                    'fecha': venta.fecha.isoformat(),
                    'metodo_pago': venta.metodo_pago,
                    'subtotal': venta.subtotal,
                    'igv': venta.igv,
                    'total': venta.total,
                    'num_detalles': len(venta.detalles)
                } for venta in ventas_paginadas.items
            ]
        }
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'message': 'Error al listar ventas', 'error': str(e)}), 500