# CrazyCine

CrazyCine é uma aplicação Flask para visualização, organização, aluguel e compra de filmes com Pix via Mercado Pago.

## Funcionalidades
- Cadastro e login de usuários
- Catálogo de filmes com busca e filtro por gênero
- Listas personalizadas, favoritos e assistir depois
- Marcar filmes como assistidos
- Compra e aluguel via Pix Mercado Pago
- Simulação de pagamento para ambiente de testes/apresentação
- Página Meus Filmes com histórico e liberação de acesso
- Testes automatizados com pytest
- Estrutura modular com Application Factory e Blueprints

## Rodar localmente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Acesse: http://127.0.0.1:5000

## Testes

```bash
pytest
```

## Deploy Render

Build Command:
```bash
pip install -r requirements.txt
```

Start Command:
```bash
gunicorn run:app
```

Variáveis de ambiente recomendadas:
- SECRET_KEY
- MERCADO_PAGO_ACCESS_TOKEN
- USE_DEMO_PIX_VALUE=true
- ENABLE_TEST_PAYMENT_SIMULATION=true
- WEBHOOK_BASE_URL=https://seu-app.onrender.com
