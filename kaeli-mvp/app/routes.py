# app/routes.py (Versión Final v4 - Votos Inteligentes)

from flask import Blueprint, jsonify, current_app, request
from .scraping import ScrapingFactory
from .models import Usuario, Carrito, Reseña
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError # Importante para manejo de errores opcional
import random
import re

bp = Blueprint('main', __name__, url_prefix='/api')
factory = ScrapingFactory()
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# --- RUTAS PÚBLICAS (Comparar, Register, Login) ---
@bp.route('/comparar/<string:producto_nombre>')
def comparar_precios(producto_nombre):
    print(f"Petición recibida para comparar: {producto_nombre}")
    try: supermercados_activos = current_app.config["KAELI_CONFIG"]["supermercados_activos"]
    except: return jsonify({"error": "Error config"}), 500
    resultados = []
    for super_nombre in supermercados_activos:
        try:
            scraper = factory.crear_scraper(super_nombre)
            res = scraper.extraer_precios(producto_nombre)
            resultados.append(res)
        except ValueError as e: resultados.append({"supermercado": super_nombre, "error": str(e)})
        except: pass
    return jsonify(resultados)

@bp.route('/register', methods=['POST'])
def register_user():
    datos = request.json
    if not datos: return jsonify({"error": "No datos"}), 400
    if not re.match(EMAIL_REGEX, datos.get('correo', '')): return jsonify({"error": "Email inválido"}), 400
    try:
        nuevo = Usuario.crear(datos.get('nombre'), datos.get('correo'), datos.get('password'))
        return jsonify({"mensaje": "Usuario creado", "id": nuevo.id_usuario}), 201
    except ValueError as e: return jsonify({"error": str(e)}), 409
    except Exception as e: return jsonify({"error": str(e)}), 500

@bp.route('/login', methods=['POST'])
def login_user():
    datos = request.json
    user = Usuario.login(datos.get('correo'), datos.get('password'))
    if user:
        token = create_access_token(identity=str(user.id_usuario))
        return jsonify({"mensaje": "Exito", "access_token": token, "usuario": {"nombre": user.nombre}}), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

# --- RUTAS PROTEGIDAS (Perfil, Carrito) ---
@bp.route('/perfil', methods=['GET'])
@jwt_required()
def get_perfil():
    return jsonify({"mensaje": f"Hola usuario {get_jwt_identity()}"}), 200

@bp.route('/carrito', methods=['GET'])
@jwt_required()
def ver_carrito():
    return jsonify(Carrito.obtener_carrito(int(get_jwt_identity()))), 200

@bp.route('/carrito/agregar', methods=['POST'])
@jwt_required()
def agregar_al_carrito():
    return jsonify(Carrito.agregar_producto(int(get_jwt_identity()), request.json)), 201

@bp.route('/carrito/restar', methods=['POST'])
@jwt_required()
def restar_del_carrito():
    return jsonify(Carrito.restar_producto(int(get_jwt_identity()), request.json)), 200

@bp.route('/carrito/eliminar', methods=['POST'])
@jwt_required()
def eliminar_del_carrito():
    return jsonify(Carrito.eliminar_producto(int(get_jwt_identity()), request.json)), 200

# --- RUTAS RESEÑAS (MODIFICADAS) ---

@bp.route('/reseñas/<string:producto_key>', methods=['GET'])
def ver_reseñas(producto_key):
    # Intentamos ver si hay un usuario logueado (opcionalmente)
    usuario_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            usuario_id = int(identity)
    except Exception:
        pass # Si no hay token o es inválido, seguimos como invitado

    try:
        reseñas = Reseña.obtener_por_producto(producto_key, usuario_id)
        return jsonify(reseñas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/reseñas', methods=['POST'])
@jwt_required()
def crear_reseña():
    id_user = int(get_jwt_identity())
    datos = request.json
    user = Usuario.query.get(id_user)
    if not user: return jsonify({"error": "Usuario no existe"}), 404
    
    try:
        nueva = Reseña.crear(id_user, user.nombre, datos.get('producto_key'), datos.get('comentario'))
        return jsonify(nueva.id_reseña), 201
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- RUTA VOTAR (TOGGLE) ---
@bp.route('/reseñas/votar/<int:id_resena>', methods=['POST'])
@jwt_required()
def votar_reseña(id_resena):
    id_user = int(get_jwt_identity())
    try:
        resultado = Reseña.toggle_voto(id_resena, id_user)
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Reseña no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- RUTA PRODUCTO (Detalle) ---
@bp.route('/producto/<string:producto_key>', methods=['GET'])
def get_detalle_producto(producto_key):
    # 1. Precios (Scraping Simulado)
    precios = []
    for super_nombre in current_app.config["KAELI_CONFIG"]["supermercados_activos"]:
        try:
            res = factory.crear_scraper(super_nombre).extraer_precios(producto_key)
            if "error" not in res: precios.append(res)
        except: pass
    
    # 2. Reseñas (Pasando usuario si existe, para ver si votó)
    usuario_id = None
    try:
        verify_jwt_in_request(optional=True)
        if get_jwt_identity(): usuario_id = int(get_jwt_identity())
    except: pass

    reseñas = Reseña.obtener_por_producto(producto_key, usuario_id)
    
    nombre = precios[0].get("producto") if precios else "Producto"
    return jsonify({"producto_key": producto_key, "nombre_generico": nombre, "precios": precios, "reseñas": reseñas}), 200

# --- ASISTENTE ---
@bp.route('/asistente/consulta', methods=['POST'])
def asistente_consulta():
    # (Simplificado para no repetir código gigante, usa la lógica de respuestas aleatorias)
    respuestas = ["Hola! Soy Kaeli.", "Busca precios en el comparador.", "Inicia sesión para el carrito."]
    return jsonify({"respuesta": random.choice(respuestas)}), 200