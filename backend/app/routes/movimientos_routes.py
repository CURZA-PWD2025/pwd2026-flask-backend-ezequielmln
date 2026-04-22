from flask import Blueprint, request
from app.controllers.movimiento_stock_controller import MovimientoStockController
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

movimientos = Blueprint('movimientos', __name__, url_prefix='/movimientos')
@movimientos.route('/')
@jwt_required()
@rol_access('admin')
def get_all():
    return MovimientoStockController.get_all()

@movimientos.route('/<int:id>', methods=['GET'])
@jwt_required()
def show(id):
    return MovimientoStockController.show(id)

@movimientos.route("/", methods=['POST'])
@jwt_required()
def create():
    return MovimientoStockController.create(request.get_json())
