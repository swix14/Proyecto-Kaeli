from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..models import Resena, Usuario, db
from .. import db
from ..models.resena import Resena
from ..models.usuario import Usuario

bp = Blueprint('resena', __name__, url_prefix='/api/resenas')

@bp.route('/<string:producto_key>', methods=['GET'])
def ver_resenas(producto_key):
    usuario_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            usuario_id = int(identity)
    except Exception:
        pass
    try:
        resenas = Resena.obtener_por_producto(producto_key, usuario_id)
        
        serializadas = [
            {
                "id_resena": r.id_resena,
                "producto_key": r.producto_key,
                "nombre_usuario": r.nombre_usuario,
                "comentario": r.comentario
            }
            for r in resenas
        ]
        return jsonify(serializadas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def crear_resena():
    id_user = int(get_jwt_identity())
    datos = request.json
    user = Usuario.query.get(id_user)
    if not user:
        return jsonify({"error": "Usuario no existe"}), 404
    try:
        nueva = Resena.crear(
            id_user,
            user.nombre,
            datos.get('producto_key'),
            datos.get('comentario')
        )
        db.session.commit()   
        return jsonify({
            "id_resena": nueva.id_resena,
            "producto_key": nueva.producto_key,
            "nombre_usuario": nueva.nombre_usuario,
            "comentario": nueva.comentario
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/vote/<int:id_resena>', methods=['POST'])
@jwt_required()
def votar_resena(id_resena):
    id_user = int(get_jwt_identity())
    try:
        resultado = Resena.toggle_voto(id_resena, id_user)
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Reseña no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
