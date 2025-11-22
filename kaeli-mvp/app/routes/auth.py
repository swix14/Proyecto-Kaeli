import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import Usuario

bp = Blueprint('auth', __name__, url_prefix='/api')

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@bp.route('/register', methods=['POST'])
def register_user():
    datos = request.json
    if not datos:
        return jsonify({"error": "No datos"}), 400
    if not re.match(EMAIL_REGEX, datos.get('correo', '')):
        return jsonify({"error": "Email inválido"}), 400
    try:
        nuevo = Usuario.crear(datos.get('nombre'), datos.get('correo'), datos.get('password'))
        return jsonify({"mensaje": "Usuario creado", "id": nuevo.id_usuario}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/login', methods=['POST'])
def login_user():
    datos = request.json
    user = Usuario.login(datos.get('correo'), datos.get('password'))
    if user:
        token = create_access_token(identity=str(user.id_usuario))
        return jsonify({"mensaje": "Exito", "access_token": token, "usuario": {"nombre": user.nombre}}), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

@bp.route('/perfil', methods=['GET'])
@jwt_required()
def get_perfil():
    return jsonify({"mensaje": f"Hola usuario {get_jwt_identity()}"}), 200
