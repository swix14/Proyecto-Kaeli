from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "correo": self.correo
        }

    @staticmethod
    def crear(nombre, correo, password_plano):
        if Usuario.query.filter_by(correo=correo).first():
            raise ValueError("El correo electrónico ya está registrado.")
        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=generate_password_hash(password_plano)
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

    @staticmethod
    def buscar_por_correo(correo):
        return Usuario.query.filter_by(correo=correo).first()

    @staticmethod
    def login(correo, password_plano):
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.password_hash, password_plano):
            return usuario
        return None
