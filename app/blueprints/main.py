from flask import Blueprint, render_template
from app.models import Movie
from app.utils import current_user

main_bp = Blueprint('main', __name__)

@main_bp.app_context_processor
def inject_user():
    return {'current_user': current_user()}

@main_bp.route('/')
def index():
    destaques = Movie.query.order_by(Movie.id.desc()).limit(4).all()
    return render_template('index.html', destaques=destaques)
