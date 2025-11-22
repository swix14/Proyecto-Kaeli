import random
from flask import Blueprint, jsonify

bp = Blueprint('asistente', __name__, url_prefix='/api')

@bp.route('/asistente/consulta', methods=['POST'])
def asistente_consulta():
    respuestas = ["Hola! Soy Kaeli.", "Busca precios en el comparador.", "Inicia sesión para el carrito."]
    return jsonify({"respuesta": random.choice(respuestas)}), 200
