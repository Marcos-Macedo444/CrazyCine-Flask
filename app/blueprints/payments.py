from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from app.extensions import db
from app.models import Movie, Transaction
from app.utils import login_required, current_user
from app.services.payments import create_pix_payment, sync_payment_status, approve_transaction

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/movies/<int:movie_id>/checkout/<action_type>', methods=['GET', 'POST'])
@login_required
def checkout(movie_id, action_type):
    movie = Movie.query.get_or_404(movie_id)
    if action_type not in ['aluguel', 'compra']:
        flash('Tipo de operação inválido.', 'danger')
        return redirect(url_for('movies.movie_detail', movie_id=movie_id))
    price = movie.rent_price if action_type == 'aluguel' else movie.buy_price
    pix_amount = current_app.config['DEMO_PIX_VALUE'] if current_app.config['USE_DEMO_PIX_VALUE'] else price
    if request.method == 'POST':
        transaction = Transaction(user_id=session['user_id'], movie_id=movie.id, type=action_type, price=price, payment_method='pix', status='pendente')
        if action_type == 'aluguel':
            transaction.expires_at = datetime.utcnow() + timedelta(days=2)
        db.session.add(transaction)
        db.session.commit()
        try:
            create_pix_payment(transaction, current_user())
        except Exception as error:
            current_app.logger.exception('Erro ao gerar Pix')
            db.session.delete(transaction)
            db.session.commit()
            flash(str(error), 'danger')
            return redirect(url_for('payments.checkout', movie_id=movie_id, action_type=action_type))
        flash('Pix gerado. O filme será liberado após aprovação do pagamento.', 'info')
        return redirect(url_for('payments.payment_pending', transaction_id=transaction.id))
    return render_template('payments/checkout.html', movie=movie, action_type=action_type, price=price, pix_amount=pix_amount)

@payments_bp.route('/pagamento/<int:transaction_id>')
@login_required
def payment_pending(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != session['user_id']:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('payments.my_movies'))
    return render_template('payments/pending.html', transaction=transaction, simulation_enabled=current_app.config['ENABLE_TEST_PAYMENT_SIMULATION'])

@payments_bp.route('/pagamento/<int:transaction_id>/verificar', methods=['POST'])
@login_required
def check_payment(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != session['user_id']:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('payments.my_movies'))
    if transaction.mp_payment_id:
        try:
            sync_payment_status(transaction.mp_payment_id)
        except Exception:
            current_app.logger.exception('Erro ao sincronizar pagamento')
    if transaction.is_released:
        flash('Pagamento aprovado! Filme liberado.', 'success')
        return redirect(url_for('payments.my_movies'))
    flash('Pagamento ainda não aprovado.', 'warning')
    return redirect(url_for('payments.payment_pending', transaction_id=transaction.id))

@payments_bp.route('/pagamento/<int:transaction_id>/simular', methods=['POST'])
@login_required
def simulate_payment(transaction_id):
    if not current_app.config['ENABLE_TEST_PAYMENT_SIMULATION']:
        flash('Simulação desativada neste ambiente.', 'danger')
        return redirect(url_for('payments.payment_pending', transaction_id=transaction_id))
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != session['user_id']:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('payments.my_movies'))
    approve_transaction(transaction)
    flash('Pagamento simulado com sucesso! Filme liberado.', 'success')
    return redirect(url_for('payments.my_movies'))

@payments_bp.route('/webhook/mercado-pago', methods=['POST', 'GET'])
def mercado_pago_webhook():
    data = request.get_json(silent=True) or {}
    payment_id = None
    if data.get('type') == 'payment':
        payment_id = (data.get('data') or {}).get('id')
    payment_id = payment_id or request.args.get('data.id') or request.args.get('id')
    if payment_id:
        try:
            sync_payment_status(str(payment_id))
        except Exception:
            current_app.logger.exception('Erro no webhook do Mercado Pago')
    return 'OK', 200

@payments_bp.route('/my-movies')
@login_required
def my_movies():
    items = Transaction.query.filter_by(user_id=session['user_id']).order_by(Transaction.created_at.desc()).all()
    return render_template('payments/my_movies.html', items=items, now=datetime.utcnow())
