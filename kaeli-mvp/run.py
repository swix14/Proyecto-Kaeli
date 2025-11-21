# run.py
# (Este archivo debe estar en el directorio raíz kaeli-mvp/)

from app import create_app

# Creamos una instancia de nuestra aplicación Flask
# llamando a la función de fábrica que está en app/__init__.py
app = create_app()

if __name__ == '__main__':
    # Ponemos debug=True para que el servidor se reinicie
    # automáticamente cuando guardes cambios y muestre errores detallados.
    app.run(debug=True)