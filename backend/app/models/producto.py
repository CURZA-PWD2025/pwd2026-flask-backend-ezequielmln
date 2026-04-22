from app.models.base_model import BaseModel
from app.models import db

class Producto(BaseModel):
    __tablename__ = "productos"
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    precio_costo = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)

    def __init__(self, nombre:str, precio_costo:float, precio_venta:float, stock_actual:int, stock_minimo:int, categoria_id:int, proveedor_id:int = None) -> None:
        self.nombre = nombre
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id
        
    def to_dict(self): 
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_costo': float(self.precio_costo),
            'precio_venta': float(self.precio_venta),
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'categoria_id': self.categoria_id,
            'proveedor_id': self.proveedor_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }