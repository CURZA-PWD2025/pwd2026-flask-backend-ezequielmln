from flask_jwt_extended import get_jwt_identity
from app.models.movimiento_stock import MovimientoStock
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller
from sqlalchemy.exc import IntegrityError

class MovimientoStockController (Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientos_stock_list = db.session.execute(db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientos_stock_list) > 0:
            movimientos_stock_to_dict = [movimiento_stock.to_dict() for movimiento_stock in movimientos_stock_list]
            return jsonify(movimientos_stock_to_dict), 200 
        return jsonify({"mensaje": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        movimiento_stock = db.session.get(MovimientoStock, id)
        if movimiento_stock:
            return jsonify(movimiento_stock.to_dict()), 200
        return jsonify({"mensaje": 'movimiento de stock no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        tipo:str = request['tipo']
        producto_id:int = request['producto_id']
        cantidad:int = request['cantidad']
        motivo:str = request['motivo']
        user_id:int = int(get_jwt_identity())
        
        error :str | None = None
        if tipo is None:
            error = 'El tipo es requerido'
        if producto_id is None:
            error = 'El producto es requerido'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if user_id is None:
            error = 'El usuario es requerido'
            
        if error is None:
            try:
                movimiento_stock = MovimientoStock(tipo=tipo, producto_id=producto_id, cantidad=cantidad, motivo=motivo, user_id=user_id)
                movimiento_stock.actualizar_stock()
                db.session.add(movimiento_stock)
                db.session.commit()
                return jsonify({'mensaje': "movimiento de stock creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'mensaje': "Error al crear el movimiento de stock"}), 409
            except ValueError as e:
                db.session.rollback()
                return jsonify({'mensaje': str(e)}), 422
        return jsonify ({'mensaje': error}), 422

    
    