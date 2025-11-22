from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..scraping.factory import ScrapingFactory
from ..models import Resena

bp = Blueprint('producto', __name__, url_prefix='/api')
factory = ScrapingFactory()

@bp.route('/comparar/<string:producto_nombre>')
def comparar_precios(producto_nombre):
    try:
        supermercados_activos = current_app.config["KAELI_CONFIG"]["supermercados_activos"]
    except Exception:
        return jsonify({"error": "Error config"}), 500
    resultados = []
    for super_nombre in supermercados_activos:
        try:
            scraper = factory.crear_scraper(super_nombre)
            res = scraper.extraer_precios(producto_nombre)
            resultados.append(res)
        except ValueError as e:
            resultados.append({"supermercado": super_nombre, "error": str(e)})
        except Exception:
            pass
    return jsonify(resultados)

@bp.route('/producto/<string:producto_key>', methods=['GET'])
def get_detalle_producto(producto_key):
    precios = []
    for super_nombre in current_app.config["KAELI_CONFIG"]["supermercados_activos"]:
        try:
            res = factory.crear_scraper(super_nombre).extraer_precios(producto_key)
            if "error" not in res:
                precios.append(res)
        except Exception:
            pass

    usuario_id = None
    try:
        verify_jwt_in_request(optional=True)
        if get_jwt_identity():
            usuario_id = int(get_jwt_identity())
    except Exception:
        pass

    resenas = Resena.obtener_por_producto(producto_key, usuario_id)
    nombre = precios[0].get("producto") if precios else "Producto"
    return jsonify({
    "producto_key": producto_key,
    "nombre_generico": nombre,
    "precios": precios,
    "reseñas": resenas   # 👈
}), 200
