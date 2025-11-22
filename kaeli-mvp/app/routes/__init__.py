from .auth import bp as auth_bp
from .carrito import bp as carrito_bp
from .resena import bp as resena_bp
from .producto import bp as producto_bp
from .asistente import bp as asistente_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(carrito_bp)
    app.register_blueprint(resena_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(asistente_bp)
