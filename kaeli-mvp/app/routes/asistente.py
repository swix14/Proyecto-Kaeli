import random
from flask import Blueprint, request, jsonify

bp = Blueprint('asistente', __name__, url_prefix='/api')

@bp.route('/asistente/consulta', methods=['POST'])
def asistente_consulta():
    data = request.get_json()
    pregunta = (data.get("consulta") or "").lower()

    # respuestas 
    respuestas_por_tema = {
        "precio": [
            "Puedes ordenar los productos por precio en la lista principal.",
            "En el comparador verás los precios de menor a mayor.",
            "Usa el botón de ordenar para ver el precio más bajo primero."
        ],
        "filtro": [
            "Marca las casillas en la barra lateral para filtrar productos.",
            "Puedes filtrar por categoría desde el menú lateral.",
            "Selecciona las categorías que quieras ver en la lista."
        ],
        "carrito": [
            "Haz clic en 'Agregar' para sumar productos al carrito.",
            "El carrito guarda lo que seleccionas en cada tienda.",
            "Puedes revisar tu carrito en la parte superior de la página."
        ],
        "reseña": [
            "En el detalle del producto puedes ver reseñas de otros compradores.",
            "Las reseñas aparecen debajo de la información del producto.",
            "Mira las opiniones en la sección de detalle para decidir mejor."
        ],
        "login": [
            "Inicia sesión para guardar tu carrito y tus preferencias.",
            "Con tu cuenta podras añadir productos al carrito.",
            "Al iniciar sesión, podras dejar reseñas en los productos."
        ]
    }

    # Buscar palabra clave
    respuesta = None
    for tema, opciones in respuestas_por_tema.items():
        if tema in pregunta:
            respuesta = random.choice(opciones)
            break

    # respuesta genérica
    if not respuesta:
        respuesta = random.choice([
            "Soy Kaeli, tu asistente de compras.",
            "Pregúntame sobre precios, filtros, carrito o reseñas.",
            "Estoy aquí para ayudarte a encontrar el mejor precio."
        ])

    return jsonify({"respuesta": respuesta}), 200
