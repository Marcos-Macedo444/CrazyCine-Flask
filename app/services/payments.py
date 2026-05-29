from datetime import datetime, timedelta
import uuid
import mercadopago
from flask import current_app, url_for
from app.extensions import db
from app.models import Transaction


def get_mp_sdk():
    token = current_app.config.get('MERCADO_PAGO_ACCESS_TOKEN', '').strip()
    if not token:
        raise RuntimeError('Configure MERCADO_PAGO_ACCESS_TOKEN para gerar Pix.')
    return mercadopago.SDK(token)


def get_webhook_url():
    base_url = current_app.config.get('WEBHOOK_BASE_URL', '').strip()
    if base_url:
        return base_url.rstrip('/') + url_for('payments.mercado_pago_webhook')
    return None


def create_pix_payment(transaction, user):
    sdk = get_mp_sdk()
    amount = current_app.config['DEMO_PIX_VALUE'] if current_app.config['USE_DEMO_PIX_VALUE'] else transaction.price
    payment_data = {
        'transaction_amount': float(amount),
        'description': f'CrazyCine - {transaction.type} - {transaction.movie.title}',
        'payment_method_id': 'pix',
        'external_reference': str(transaction.id),
        'payer': {
            'email': user.email,
            'first_name': user.name.split()[0] if user.name else 'Cliente'
        }
    }
    webhook_url = get_webhook_url()
    if webhook_url:
        payment_data['notification_url'] = webhook_url

    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {'x-idempotency-key': str(uuid.uuid4())}
    result = sdk.payment().create(payment_data, request_options)
    response = result.get('response', {})

    if result.get('status') not in [200, 201] or 'id' not in response:
        raise RuntimeError(f'Erro ao criar pagamento Pix: {response}')

    tx_data = response.get('point_of_interaction', {}).get('transaction_data', {})
    transaction.mp_payment_id = str(response.get('id'))
    transaction.status = 'pendente'
    transaction.pix_qr_code = tx_data.get('qr_code')
    transaction.pix_qr_code_base64 = tx_data.get('qr_code_base64')
    db.session.commit()
    return transaction


def approve_transaction(transaction):
    if transaction.status == 'aprovado':
        return transaction
    transaction.status = 'aprovado'
    if transaction.type == 'aluguel':
        transaction.expires_at = datetime.utcnow() + timedelta(days=2)
    db.session.commit()
    return transaction


def sync_payment_status(mp_payment_id):
    sdk = get_mp_sdk()
    result = sdk.payment().get(mp_payment_id)
    response = result.get('response', {})
    status = response.get('status')
    transaction = Transaction.query.filter_by(mp_payment_id=str(mp_payment_id)).first()
    if transaction and status == 'approved':
        approve_transaction(transaction)
    elif transaction and status in ['rejected', 'cancelled', 'refunded', 'charged_back']:
        transaction.status = status
        db.session.commit()
    return transaction
