import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'crazycine-dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{INSTANCE_DIR / 'crazycine.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN', '')
    WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', '')
    USE_DEMO_PIX_VALUE = os.getenv('USE_DEMO_PIX_VALUE', 'true').lower() == 'true'
    DEMO_PIX_VALUE = float(os.getenv('DEMO_PIX_VALUE', '0.01'))
    ENABLE_TEST_PAYMENT_SIMULATION = os.getenv('ENABLE_TEST_PAYMENT_SIMULATION', 'true').lower() == 'true'
    WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED', 'true').lower() == 'true'

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
