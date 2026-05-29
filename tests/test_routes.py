import pytest
from app import create_app
from app.extensions import db
from app.models import Movie, User, Transaction
from config import TestConfig

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

def register_and_login(client):
    client.post('/register', data={
        'name': 'Usuario Teste',
        'email': 'teste@example.com',
        'password': '123456',
        'confirm_password': '123456'
    }, follow_redirects=True)
    return client.post('/login', data={'email': 'teste@example.com', 'password': '123456'}, follow_redirects=True)

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'CrazyCine' in response.data

def test_register_login_dashboard(client):
    response = register_and_login(client)
    assert response.status_code == 200
    assert 'Dashboard'.encode() in response.data

def test_movies_requires_login(client):
    response = client.get('/movies', follow_redirects=True)
    assert b'login' in response.data.lower() or 'Faça login'.encode() in response.data

def test_movie_catalog_after_login(client):
    register_and_login(client)
    response = client.get('/movies')
    assert response.status_code == 200
    assert b'Interestelar' in response.data

def test_simulate_payment_releases_movie(client, app):
    register_and_login(client)
    with app.app_context():
        user = User.query.filter_by(email='teste@example.com').first()
        movie = Movie.query.first()
        tx = Transaction(user_id=user.id, movie_id=movie.id, type='compra', price=movie.buy_price, status='pendente')
        db.session.add(tx)
        db.session.commit()
        tx_id = tx.id
    response = client.post(f'/pagamento/{tx_id}/simular', follow_redirects=True)
    assert response.status_code == 200
    assert 'Pagamento simulado'.encode() in response.data
    with app.app_context():
        assert Transaction.query.get(tx_id).status == 'aprovado'
