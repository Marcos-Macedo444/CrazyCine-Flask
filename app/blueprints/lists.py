from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db
from app.forms import ListForm
from app.models import MovieList, Movie
from app.utils import login_required

lists_bp = Blueprint('lists', __name__)

@lists_bp.route('/lists')
@login_required
def lists():
    form = ListForm()
    user_lists = MovieList.query.filter_by(user_id=session['user_id']).order_by(MovieList.name).all()
    return render_template('lists/lists.html', user_lists=user_lists, form=form)

@lists_bp.route('/lists/create', methods=['POST'])
@login_required
def create_list():
    form = ListForm()
    if form.validate_on_submit():
        db.session.add(MovieList(name=form.name.data.strip(), user_id=session['user_id']))
        db.session.commit()
        flash('Lista criada com sucesso.', 'success')
    else:
        flash('Digite um nome válido para a lista.', 'danger')
    return redirect(url_for('lists.lists'))

@lists_bp.route('/lists/<int:list_id>')
@login_required
def list_detail(list_id):
    movie_list = MovieList.query.get_or_404(list_id)
    if movie_list.user_id != session['user_id']:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('lists.lists'))
    return render_template('lists/detail.html', movie_list=movie_list)

@lists_bp.route('/lists/<int:list_id>/delete', methods=['POST'])
@login_required
def delete_list(list_id):
    movie_list = MovieList.query.get_or_404(list_id)
    if movie_list.user_id != session['user_id']:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('lists.lists'))
    db.session.delete(movie_list)
    db.session.commit()
    flash('Lista removida.', 'info')
    return redirect(url_for('lists.lists'))

@lists_bp.route('/movies/<int:movie_id>/add-to-list', methods=['POST'])
@login_required
def add_to_list(movie_id):
    from app.forms import AddToListForm
    form = AddToListForm()
    user_lists = MovieList.query.filter_by(user_id=session['user_id']).all()
    form.list_id.choices = [(lst.id, lst.name) for lst in user_lists]
    movie = Movie.query.get_or_404(movie_id)
    if form.validate_on_submit():
        movie_list = MovieList.query.get_or_404(form.list_id.data)
        if movie_list.user_id != session['user_id']:
            flash('Acesso negado.', 'danger')
        elif movie not in movie_list.movies:
            movie_list.movies.append(movie)
            db.session.commit()
            flash('Filme adicionado à lista.', 'success')
        else:
            flash('Este filme já está na lista.', 'warning')
    else:
        flash('Selecione uma lista válida.', 'danger')
    return redirect(url_for('movies.movie_detail', movie_id=movie_id))

@lists_bp.route('/lists/<int:list_id>/remove/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_list(list_id, movie_id):
    movie_list = MovieList.query.get_or_404(list_id)
    movie = Movie.query.get_or_404(movie_id)
    if movie_list.user_id != session['user_id']:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('lists.lists'))
    if movie in movie_list.movies:
        movie_list.movies.remove(movie)
        db.session.commit()
        flash('Filme removido da lista.', 'info')
    return redirect(url_for('lists.list_detail', list_id=list_id))
