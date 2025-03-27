from flask import Blueprint, request, jsonify
from funtion_jwt import write_token, validate_token

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Acceder al username correctamente
    if data.get('username') == 'Duran':
        return write_token(data=data)
    else:
        response = {
            "message": "user not found"
        }
        return jsonify(response), 404

@routes_auth.route('/verify/token')
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)