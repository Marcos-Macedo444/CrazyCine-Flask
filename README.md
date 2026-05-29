# README.md

# 🎬 CrazyCine

CrazyCine é uma plataforma web desenvolvida com Flask que permite aos usuários explorar um catálogo de filmes, criar listas personalizadas, marcar filmes como assistidos e simular compras ou aluguéis utilizando Pix.

---

# 🚀 Funcionalidades

* Cadastro e login de usuários
* Catálogo completo de filmes
* Busca por nome
* Filtro por gênero
* Página de detalhes dos filmes
* Criação de listas personalizadas
* Controle de filmes assistidos
* Sistema de compra e aluguel
* Integração com Mercado Pago
* Dashboard do usuário
* Interface responsiva

---

# 🛠️ Tecnologias Utilizadas

* Python
* Flask
* SQLAlchemy
* Jinja2
* Bootstrap 5
* SQLite/PostgreSQL
* Mercado Pago API
* Render

---

# 📁 Estrutura do Projeto

```txt id="1bplxw"
CrazyCine-Flask/
│
├── app/
│   ├── blueprints/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── forms.py
│   ├── seed.py
│   ├── utils.py
│   └── __init__.py
│
├── instance/
├── migrations/
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

---

# ⚙️ Como Rodar o Projeto

## 1. Clonar o repositório

```bash id="o9j2lq"
git clone https://github.com/Marcos-Macedo444/CrazyCine-Flask.git
```

---

## 2. Entrar na pasta

```bash id="g9c7pv"
cd CrazyCine-Flask
```

---

## 3. Criar ambiente virtual

```bash id="7zznq2"
python -m venv venv
```

---

## 4. Ativar ambiente virtual

### Windows

```bash id="ujcb9g"
venv\Scripts\activate
```

### Linux/Mac

```bash id="3ic5qt"
source venv/bin/activate
```

---

## 5. Instalar dependências

```bash id="x4r9nk"
pip install -r requirements.txt
```

---

## 6. Configurar variáveis de ambiente

```env id="2l5o9m"
SECRET_KEY=sua_chave
DATABASE_URL=seu_banco
WEBHOOK_BASE_URL=url_do_render
```

---

## 7. Executar o projeto

```bash id="ck7u0k"
python run.py
```

---

# 🌐 Deploy

O projeto foi publicado utilizando Render.

---

# 👨‍💻 Integrantes

* Marcos Filipe de Paula Macêdo
* Tailon Cypreste
* Pedro Henrique Amorim

---

# 🔗 GitHub

https://github.com/Marcos-Macedo444/CrazyCine-Flask.git
