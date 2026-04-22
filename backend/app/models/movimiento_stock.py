from app.models import db
from app.models.base_model import BaseModel
from sqlalchemy import CheckConstraint
from app.models.producto import Producto

class MovimientoStock(BaseModel):
    __tablename__ = "movimientos_stock"
    tipo = db.Column(db.String(10), nullable=False)  #entrada o salida
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    producto= db.relationship('Producto')
    user = db.relationship('User')

    tipos = ("entrada", "salida")
    
    def __init__(self, tipo:str, producto_id:int, cantidad:int, motivo: str, user_id:int) -> None:
        if tipo not in self.tipos:
            raise ValueError(f"Tipo {tipo} inválido. Debe ser entrada o salida")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        self.tipo = tipo
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.motivo = motivo
        self.user_id = user_id
        
    def actualizar_stock(self):
        producto = db.session.get(Producto, self.producto_id)
        if not producto:
            raise ValueError(f"Producto con id {self.producto_id} no encontrado")
        if self.tipo == "entrada":
            producto.stock_actual += self.cantidad
        elif self.tipo == "salida":
            if producto.stock_actual < self.cantidad:
                raise ValueError(f"Stock insuficiente. Stock actual: {producto.stock_actual}")
            producto.stock_actual -= self.cantidad
        
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'motivo': self.motivo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        