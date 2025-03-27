from flask import Flask
from utils.db import db
from routes.marcas import marcas
from routes.categoriasRoute import categorias
from routes.productoRoutes import productos
from routes.proveedorRoutes import proveedor
from routes.compraRoutes import compras
from routes.detalleCompraRoutes import detalle_compra
from routes.auth import routes_auth
from flask_cors import CORS
from config import DATABASE_CONECCTION_URI

app = Flask(__name__)
CORS(marcas, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONECCTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(marcas, url_prefix='/api/marca')
app.register_blueprint(categorias, url_prefix='/api/categoria')
app.register_blueprint(productos, url_prefix='/api/producto')
app.register_blueprint(proveedor, url_prefix='/api/proveedor')
app.register_blueprint(compras, url_prefix='/api/compra')
app.register_blueprint(detalle_compra, url_prefix='/api/detallecompra')
app.register_blueprint(routes_auth, url_prefix='/api')

@app.get('/')
def home():
    return 'Hello word'

