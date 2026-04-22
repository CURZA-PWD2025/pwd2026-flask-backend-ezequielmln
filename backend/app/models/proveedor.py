from app.models.base_model import BaseModel
from app.models import db   

class Proveedor(BaseModel):
    __tablename__ = "proveedores" 
    nombre = db.Column(db.String(150), nullable=False)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    
    def __init__(self, nombre:str, telefono:str = None) -> None:
        self.nombre = nombre
        self.telefono = telefono
        
    def to_dict(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'contacto': self.contacto,
            'telefono': self.telefono,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }