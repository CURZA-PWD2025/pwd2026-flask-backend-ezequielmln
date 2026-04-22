from app.models.proveedor import Proveedor
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller
from sqlalchemy.exc import IntegrityError

class ProveedorController (Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        proveedores_list = db.session.execute(db.select(Proveedor).order_by(db.desc(Proveedor.id))).scalars().all()
        if len(proveedores_list) > 0:
            proveedores_to_dict = [proveedor.to_dict() for proveedor in proveedores_list]
            return jsonify(proveedores_to_dict), 200 
        return jsonify({"mensaje": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor:
            return jsonify(proveedor.to_dict()), 200
        return jsonify({"mensaje": 'proveedor no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request['nombre']
        contacto:str = request['contacto']
        telefono:str = request['telefono']
        email:str = request['email']
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
            
        if error is None:
            try:
                proveedor = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono, email=email)
                db.session.add(proveedor)
                db.session.commit()
                return jsonify({'mensaje': "proveedor creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'mensaje': "Proveedor ya registrado"}), 409
        return jsonify ({'mensaje': error}), 422
        
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request['nombre']
        contacto:str = request['contacto']
        telefono:str = request['telefono']
        email:str = request['email']
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
            
        if error is None:
            proveedor = db.session.get(Proveedor, id)
            if proveedor:
                try:
                    proveedor.nombre = nombre
                    proveedor.contacto = contacto
                    proveedor.telefono = telefono
                    proveedor.email = email
                    db.session.commit()
                    return jsonify({'mensaje':'proveedor modificado con exito'}), 200
                except IntegrityError:
                    error = 'el email o el username ya existen' 
                    return jsonify({'mensaje':error}), 409
                    
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
    
        if proveedor is None:
            return jsonify({'mensaje': 'proveedor no encontrado'}), 404
    
        if len(proveedor.productos) > 0:
            return jsonify({'mensaje': 'no se puede eliminar el proveedor porque tiene productos asociados'}), 409
    
        db.session.delete(proveedor)
        db.session.commit()
        return jsonify({'mensaje': 'el proveedor fue eliminado con exito'}), 200