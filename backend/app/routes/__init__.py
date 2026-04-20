from app.routes.auth_routes import auth_bp
from app.routes.rol_routes import roles
from app.routes.user_routes import users 
from app.routes.categoria_routes import categorias
from app.routes.productos_routes import productos
from app.routes.movimientos_routes import movimientos
from app.routes.proveedores_routes import proveedores
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')

api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(users)
api_v1.register_blueprint(roles)
api_v1.register_blueprint(categorias)
api_v1.register_blueprint(productos)
api_v1.register_blueprint(movimientos)
api_v1.register_blueprint(proveedores)
