from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError


class Login(FlaskForm):
	usuario = StringField("Usuario", validators=[DataRequired(message="Informe seu Usuario!")])
	senha = PasswordField("Senha", validators=[DataRequired(message="Infome  sua Senha!")])
	lembrar = BooleanField("lembrar usuário")
	botao_logar = SubmitField("Login")


class Form_Os(FlaskForm):
	marca = StringField("Marca")
	modelo = StringField("Modelo")
	ano = StringField("Ano")
	versao = StringField("Versão")
	cor = StringField("Cor")
	placa = StringField("Placa")
	motor = StringField("Motor")
	tipo = StringField("Tipo")
	Obs = StringField("Observações")
	