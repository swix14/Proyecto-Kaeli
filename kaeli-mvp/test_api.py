import pytest
from app import create_app, db
from app.models.usuario import Usuario
from app.models.resena import Resena
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
# ------------------------
# FIXTURES
# ------------------------

@pytest.fixture
def app():
    """Crea la aplicación en modo testing con BD en memoria"""
    app = create_app(testing=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de pruebas para simular requests HTTP"""
    return app.test_client()


@pytest.fixture
def usuario_test(app):
    """Crea un usuario de prueba en la BD"""
    with app.app_context():
        user = Usuario(
            id_usuario=4,
            nombre="Sebastián",
            correo="test@test.com",
            password_hash=generate_password_hash("test123")
        )
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id_usuario)
        return user


@pytest.fixture
def token(app, usuario_test):
    """Genera un JWT válido para el usuario de prueba"""
    with app.app_context():
        return create_access_token(identity=usuario_test.id_usuario)

# ------------------------
# TESTS
# ------------------------

def test_crear_resena(client, app):
    # Crear usuario en la BD de prueba
    with app.app_context():
        user = Usuario(id_usuario=4, nombre="Sebastián", correo="test@test.com")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id_usuario)

    # Enviar reseña con JWT válido
    res = client.post("/api/resenas",
                      json={"producto_key": "arroz", "comentario": "Muy buen producto"},
                      headers={"Authorization": f"Bearer {token}"})

    # Depuración si falla
    print(res.get_data(as_text=True))

    assert res.status_code == 201
    data = res.get_json()
    assert data["comentario"] == "Muy buen producto"
    assert data["producto_key"] == "arroz"
    assert data["nombre_usuario"] == "Sebastián"



def test_ver_resenas(client):
    res = client.get("/api/resenas/arroz")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)


def test_votar_resena(client, app, token, usuario_test):
    with app.app_context():
        nueva = Resena.crear(usuario_test.id_usuario, usuario_test.nombre, "arroz", "Excelente")
        db.session.commit()
        resena_id = nueva.id_resena  # guardar ID antes de salir del contexto

    res = client.post(f"/api/resenas/vote/{resena_id}",
                      headers={"Authorization": f"Bearer {token}"})
    print(res.status_code)
    print(res.get_data(as_text=True))

    assert res.status_code == 200
    data = res.get_json()
    assert "total" in data


def test_detalle_producto(client):
    res = client.get("/api/productos/arroz")
    assert res.status_code == 200
    data = res.get_json()
    assert data["producto_key"] == "arroz"
