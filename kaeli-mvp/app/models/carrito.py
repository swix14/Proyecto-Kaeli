from ..extensions import db

class CarritoItem(db.Model):
    __tablename__ = 'carrito_items'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    supermercado = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, default=1)
