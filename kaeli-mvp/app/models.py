# app/models.py (Versión Final v4 - Votos Únicos con Toggle)

from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# ---
# TABLA DE ASOCIACIÓN (Muchos a Muchos)
# ---
# Esta tabla guarda quién votó qué. No es una clase, es una tabla auxiliar.
tabla_votos = db.Table('votos',
    db.Column('user_id', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('reseñas.id_reseña'), primary_key=True)
)

# ---
# CLASE 1: USUARIO
# ---
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


# ---
# CLASE 2: CARRITO (Sin cambios en lógica, solo importaciones)
# ---
class CarritoItem(db.Model):
    __tablename__ = 'carrito_items'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    supermercado = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, default=1)

class Carrito:
    @staticmethod
    def obtener_carrito(id_usuario):
        items_sql = CarritoItem.query.filter_by(usuario_id=id_usuario).all()
        items_frontend = []
        total_carrito = 0
        cantidad_items_unicos = len(items_sql) 
        for item in items_sql:
            items_frontend.append({
                "nombre": item.nombre,
                "precio": item.precio,
                "supermercado": item.supermercado,
                "cantidad": item.cantidad
            })
            total_carrito += (item.precio * item.cantidad)
        return { "items": items_frontend, "total": total_carrito, "cantidad_items": cantidad_items_unicos }

    @staticmethod
    def agregar_producto(id_usuario, producto_data):
        nombre = producto_data.get('nombre')
        supermercado = producto_data.get('supermercado')
        precio = producto_data.get('precio')
        if not nombre or not supermercado: raise ValueError("Datos inválidos.")
        item = CarritoItem.query.filter_by(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado).first()
        if item: item.cantidad += 1
        else:
            nuevo_item = CarritoItem(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado, precio=precio, cantidad=1)
            db.session.add(nuevo_item)
        db.session.commit()
        return Carrito.obtener_carrito(id_usuario)

    @staticmethod
    def restar_producto(id_usuario, producto_data):
        nombre = producto_data.get('nombre')
        supermercado = producto_data.get('supermercado')
        item = CarritoItem.query.filter_by(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado).first()
        if not item: raise ValueError("Producto no encontrado.")
        if item.cantidad > 1: item.cantidad -= 1
        else: db.session.delete(item)
        db.session.commit()
        return Carrito.obtener_carrito(id_usuario)

    @staticmethod
    def eliminar_producto(id_usuario, producto_data):
        nombre = producto_data.get('nombre')
        supermercado = producto_data.get('supermercado')
        item = CarritoItem.query.filter_by(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado).first()
        if item:
            db.session.delete(item)
            db.session.commit()
        return Carrito.obtener_carrito(id_usuario)


# ---
# CLASE 3: RESEÑA (Maneja reseñas.json) - ¡MODIFICADA!
# ---
class Reseña(db.Model):
    __tablename__ = 'reseñas'
    
    id_reseña = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    nombre_usuario = db.Column(db.String(100)) 
    producto_key = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    
    # Relación: Una reseña tiene muchos votantes (Usuarios)
    votantes = db.relationship('Usuario', secondary=tabla_votos, backref='votos_dados', lazy='dynamic')

    @property
    def total_votos(self):
        return self.votantes.count()

    @staticmethod
    def obtener_por_producto(producto_key, usuario_actual_id=None):
        reseñas_sql = Reseña.query.filter_by(producto_key=producto_key.lower()).all()
        lista_reseñas = []
        
        for r in reseñas_sql:
            # Verificamos si el usuario actual (si existe) ya votó esta reseña
            ya_vote = False
            if usuario_actual_id:
                usuario = Usuario.query.get(usuario_actual_id)
                # Chequeo eficiente en la BD
                if usuario and r.votantes.filter_by(id_usuario=usuario.id_usuario).first():
                    ya_vote = True

            lista_reseñas.append({
                "id_reseña": r.id_reseña,
                "nombre_usuario": r.nombre_usuario,
                "comentario": r.comentario,
                "votos_utiles": r.total_votos, # Usamos la propiedad dinámica
                "ya_vote": ya_vote # Para que el frontend sepa pintar el botón
            })
        return lista_reseñas

    @staticmethod
    def toggle_voto(id_reseña, id_usuario):
        """
        (RF09) Si ya votó, quita el voto. Si no, lo pone.
        Devuelve el nuevo total y el estado (agregado/quitado).
        """
        reseña = Reseña.query.get(id_reseña)
        usuario = Usuario.query.get(id_usuario)

        if not reseña or not usuario:
            return None

        # Verificamos si ya votó
        if reseña.votantes.filter_by(id_usuario=id_usuario).first():
            # Ya votó -> Quitamos el voto
            reseña.votantes.remove(usuario)
            accion = "quitado"
        else:
            # No ha votado -> Agregamos el voto
            reseña.votantes.append(usuario)
            accion = "agregado"
            
        db.session.commit()
        
        return {
            "total": reseña.total_votos,
            "accion": accion
        }

    @staticmethod
    def crear(id_usuario, nombre_usuario, producto_key, comentario):
        if not comentario or not producto_key:
            raise ValueError("Faltan datos.")
            
        nueva_reseña = Reseña(
            id_usuario=id_usuario,
            nombre_usuario=nombre_usuario,
            producto_key=producto_key.lower(),
            comentario=comentario
        )
        db.session.add(nueva_reseña)
        db.session.commit()
        return nueva_reseña