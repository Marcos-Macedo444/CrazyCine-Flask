from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.forms import AddToListForm
from app.models import Movie, MovieList, WatchedMovie, Transaction
from app.utils import login_required, current_user

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    return render_template('movies/dashboard.html',
        total_lists=MovieList.query.filter_by(user_id=user.id).count(),
        total_watched=WatchedMovie.query.filter_by(user_id=user.id).count(),
        total_movies=Movie.query.count(),
        total_orders=Transaction.query.filter_by(user_id=user.id).count(),
        recent_movies=Movie.query.order_by(Movie.id.desc()).limit(4).all()
    )

@movies_bp.route('/movies')
@login_required
def movies():
    query = request.args.get('q', '').strip()
    genre = request.args.get('genre', '').strip()
    movies_query = Movie.query
    if query:
        movies_query = movies_query.filter(Movie.title.ilike(f'%{query}%'))
    if genre:
        movies_query = movies_query.filter(Movie.genre.ilike(f'%{genre}%'))
    genres = sorted({movie.genre for movie in Movie.query.all()})
    return render_template('movies/movies.html', movies=movies_query.order_by(Movie.title).all(), query=query, genre=genre, genres=genres)

@movies_bp.route('/movies/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = AddToListForm()
    user_lists = MovieList.query.filter_by(user_id=session['user_id']).all()
    form.list_id.choices = [(lst.id, lst.name) for lst in user_lists]
    watched = WatchedMovie.query.filter_by(user_id=session['user_id'], movie_id=movie_id).first() is not None
    purchased = Transaction.query.filter_by(user_id=session['user_id'], movie_id=movie_id, type='compra', status='aprovado').first() is not None
    active_rental = Transaction.query.filter(Transaction.user_id == session['user_id'], Transaction.movie_id == movie_id, Transaction.type == 'aluguel', Transaction.status == 'aprovado', Transaction.expires_at > datetime.utcnow()).first()
    return render_template('movies/detail.html', movie=movie, form=form, watched=watched, purchased=purchased, active_rental=active_rental)

@movies_bp.route('/movies/<int:movie_id>/toggle-watched', methods=['POST'])
@login_required
def toggle_watched(movie_id):
    watched = WatchedMovie.query.filter_by(user_id=session['user_id'], movie_id=movie_id).first()
    if watched:
        db.session.delete(watched)
        flash('Filme desmarcado como assistido.', 'info')
    else:
        db.session.add(WatchedMovie(user_id=session['user_id'], movie_id=movie_id))
        flash('Filme marcado como assistido.', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('movies.movies'))

@movies_bp.route('/watched')
@login_required
def watched():
    watched_items = WatchedMovie.query.filter_by(user_id=session['user_id']).all()
    return render_template('movies/watched.html', watched_items=watched_items)
