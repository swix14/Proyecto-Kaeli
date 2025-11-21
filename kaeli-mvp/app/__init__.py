# app/__init__.py

from flask import Flask, render_template
from .config import config_global
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Inicializamos la variable de la BD
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = "kaeli-mvp-super-secreto-2025" 
    
    # Configuración de BD
    app.config["SQLALCHEMY_DATABASE_URI"] = config_global.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    jwt = JWTManager(app)
    db.init_app(app)
    
    app.config["KAELI_CONFIG"] = config_global.mostrar_configuracion()
    
    print("Configuración de Kaeli cargada:")
    print(app.config["KAELI_CONFIG"])

    with app.app_context():
        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
        # Importamos los modelos explícitamente para que SQLAlchemy los "vea"
        from . import models 
        from . import routes
        
        # Ahora sí, crea las tablas
        try:
            db.create_all()
            print(">>> ÉXITO: Tablas creadas en PostgreSQL.")
        except Exception as e:
            print(f">>> ERROR FATAL en BD: {e}")

        app.register_blueprint(routes.bp)

    @app.route('/hello')
    def hello():
        return '¡Hola! Kaeli MVP está funcionando con PostgreSQL.'

    @app.route('/')
    def index():
        return render_template('index.html')

    return app