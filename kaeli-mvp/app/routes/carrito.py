from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import CarritoItem
from ..extensions import db

bp = Blueprint('carrito', __name__, url_prefix='/api')

# Funciones del carrito basadas en tu lógica original
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
    return {"items": items_frontend, "total": total_carrito, "cantidad_items": cantidad_items_unicos}

@bp.route('/carrito', methods=['GET'])
@jwt_required()
def ver_carrito():
    return jsonify(obtener_carrito(int(get_jwt_identity()))), 200

@bp.route('/carrito/agregar', methods=['POST'])
@jwt_required()
def agregar_al_carrito():
    id_usuario = int(get_jwt_identity())
    datos = request.json
    nombre = datos.get('nombre')
    supermercado = datos.get('supermercado')
    precio = datos.get('precio')
    if not nombre or not supermercado:
        return jsonify({"error": "Datos inválidos."}), 400
    item = CarritoItem.query.filter_by(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado).first()
    if item:
        item.cantidad += 1
    else:
        nuevo_item = CarritoItem(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado, precio=precio, cantidad=1)
        db.session.add(nuevo_item)
    db.session.commit()
    return jsonify(obtener_carrito(id_usuario)), 201

@bp.route('/carrito/restar', methods=['POST'])
@jwt_required()
def restar_del_carrito():
    id_usuario = int(get_jwt_identity())
    datos = request.json
    nombre = datos.get('nombre')
    supermercado = datos.get('supermercado')
    item = CarritoItem.query.filter_by(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado).first()
    if not item:
        return jsonify({"error": "Producto no encontrado."}), 404
    if item.cantidad > 1:
        item.cantidad -= 1
    else:
        db.session.delete(item)
    db.session.commit()
    return jsonify(obtener_carrito(id_usuario)), 200

@bp.route('/carrito/eliminar', methods=['POST'])
@jwt_required()
def eliminar_del_carrito():
    id_usuario = int(get_jwt_identity())
    datos = request.json
    nombre = datos.get('nombre')
    supermercado = datos.get('supermercado')
    item = CarritoItem.query.filter_by(usuario_id=id_usuario, nombre=nombre, supermercado=supermercado).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify(obtener_carrito(id_usuario)), 200
