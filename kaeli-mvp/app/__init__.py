# app/__init__.py
import os
from flask import Flask, render_template
from .config import config_global
from .extensions import db, jwt
from flask_migrate import Migrate

def create_app(testing=False):
    app = Flask(__name__)

    # Configuración
    app.config["JWT_SECRET_KEY"] = config_global.api_key
    app.config["SQLALCHEMY_DATABASE_URI"] = config_global.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

     # Guardar configuración Kaeli en app.config
    app.config["KAELI_CONFIG"] = config_global.mostrar_configuracion()

    # Registrar blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    # Ruta principal para mostrar index.html
    @app.route("/")
    def index():
        return render_template("index.html")

    # Ruta de prueba opcional
    @app.route("/hello")
    def hello():
        return "¡Hola! Kaeli MVP está funcionando con PostgreSQL."

    return app
