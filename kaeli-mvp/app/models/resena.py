from ..extensions import db
from .usuario import Usuario

# Tabla de asociación para votos (muchos a muchos)
tabla_votos = db.Table(
    'votos',
    db.Column('user_id', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('resenas.id_resena'), primary_key=True)
)

class Resena(db.Model):
    __tablename__ = 'resenas'  

    id_resena = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    nombre_usuario = db.Column(db.String(100))
    producto_key = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.Text, nullable=False)

    votantes = db.relationship('Usuario', secondary=tabla_votos, backref='votos_dados', lazy='dynamic')

    @property
    def total_votos(self):
        return self.votantes.count()

    @staticmethod
    def obtener_por_producto(producto_key, usuario_actual_id=None):
        resenas_sql = Resena.query.filter_by(producto_key=producto_key.lower()).all()
        lista_resenas = []

        for r in resenas_sql:
            ya_vote = False
            if usuario_actual_id:
                usuario = Usuario.query.get(usuario_actual_id)
                if usuario and r.votantes.filter_by(id_usuario=usuario.id_usuario).first():
                    ya_vote = True

            lista_resenas.append({
                "id_resena": r.id_resena,
                "nombre_usuario": r.nombre_usuario,
                "comentario": r.comentario,
                "votos_utiles": r.total_votos,
                "ya_vote": ya_vote
            })
        return lista_resenas

    @staticmethod
    def toggle_voto(id_resena, id_usuario):
        resena = Resena.query.get(id_resena)
        usuario = Usuario.query.get(id_usuario)

        if not resena or not usuario:
            return None

        if resena.votantes.filter_by(id_usuario=id_usuario).first():
            resena.votantes.remove(usuario)
            accion = "quitado"
        else:
            resena.votantes.append(usuario)
            accion = "agregado"

        db.session.commit()
        return {"total": resena.total_votos, "accion": accion}

    @staticmethod
    def crear(id_usuario, nombre_usuario, producto_key, comentario):
        if not comentario or not producto_key:
            raise ValueError("Faltan datos.")
        nueva_resena = Resena(
            id_usuario=id_usuario,
            nombre_usuario=nombre_usuario,
            producto_key=producto_key.lower(),
            comentario=comentario
        )
        db.session.add(nueva_resena)
        db.session.commit()
        return nueva_resena
