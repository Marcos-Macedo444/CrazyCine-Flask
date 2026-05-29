from datetime import datetime
from .extensions import db

list_movies = db.Table(
    'list_movies',
    db.Column('list_id', db.Integer, db.ForeignKey('movie_list.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    lists = db.relationship('MovieList', backref='user', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', cascade='all, delete-orphan')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(120), nullable=False)
    poster_url = db.Column(db.String(300))
    rent_price = db.Column(db.Float, nullable=False, default=7.90)
    buy_price = db.Column(db.Float, nullable=False, default=29.90)

class MovieList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movies = db.relationship('Movie', secondary=list_movies, lazy='subquery', backref=db.backref('movie_lists', lazy=True))

class WatchedMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # aluguel ou compra
    price = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(40), nullable=False, default='pix')
    status = db.Column(db.String(30), nullable=False, default='pendente')
    mp_payment_id = db.Column(db.String(80), unique=True)
    pix_qr_code = db.Column(db.Text)
    pix_qr_code_base64 = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    movie = db.relationship('Movie')

    @property
    def is_released(self):
        if self.status != 'aprovado':
            return False
        if self.type == 'compra':
            return True
        return self.expires_at and self.expires_at > datetime.utcnow()
