from app.models.categoria import Categoria
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller 
from sqlalchemy.exc import IntegrityError

class CategoriaController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        categorias_list = db.session.execute(db.select(Categoria).order_by(db.desc(Categoria.id))).scalars().all()
        if len(categorias_list) > 0:
            categorias_to_dict = [categoria.to_dict() for categoria in categorias_list]
            return jsonify(categorias_to_dict), 200 
        return jsonify({"mensaje": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria:
            return jsonify(categoria.to_dict()), 200
        return jsonify({"mensaje": 'categoria no encontrada'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request['nombre']
        descripcion:str = request['descripcion']
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
            
        if error is None:
            try:
                categoria = Categoria(nombre=nombre, descripcion=descripcion)
                db.session.add(categoria)
                db.session.commit()
                return jsonify({'mensaje': "categoria creada con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'mensaje': "Categoria ya registrada"}), 409
        return jsonify ({'mensaje': error}), 422
        
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request['nombre']
        descripcion:str = request['descripcion']
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if descripcion is None:
            error = 'La descripcion es requerida'
            
        if error is None:
            categoria = db.session.get(Categoria, id)
            if categoria:
                try:
                    categoria.nombre = nombre
                    categoria.descripcion = descripcion
                    db.session.commit()
                    return jsonify({'mensaje':'categoria modificada con exito'}), 200
                except IntegrityError:
                    error = 'la categoria ya existe' 
                    return jsonify({'mensaje':error}), 409
            else:     
                error = 'categoria no encontrada'
            
        return jsonify({'mensaje':error}), 404
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
    
        if categoria is None:
            return jsonify({'mensaje': 'categoria no encontrada'}), 404
    
        if len(categoria.productos) > 0:
            return jsonify({'mensaje': 'no se puede eliminar la categoria porque tiene productos asociados'}), 409
    
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'mensaje': 'la categoria fue eliminada con exito'}), 200