from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password', message='As senhas não conferem.')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ListForm(FlaskForm):
    name = StringField('Nome da lista', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Criar lista')

class AddToListForm(FlaskForm):
    list_id = SelectField('Lista', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Adicionar')
