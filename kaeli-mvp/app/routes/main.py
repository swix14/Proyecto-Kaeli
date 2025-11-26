from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    # Renderiza página principal 
    return render_template("index.html")

@bp.route("/login")
def login_page():
    return render_template("login.html")

@bp.route("/register")
def register_page():
    return render_template("register.html")

@bp.route("/detalle/<product_key>")
def detalle(product_key):
    
    return render_template("detail.html", product_key=product_key)
