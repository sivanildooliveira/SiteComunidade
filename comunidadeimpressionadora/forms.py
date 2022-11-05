from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuarios
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')
    
    def validate_email(self, email):
        usuario = Usuarios.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já Cadastrado! tente outro E-mail.')
    
    def validate_username(self, username):
        usuario = Usuarios.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("Nome de usuario já existe! Tente outro username.")


class FormLogin(FlaskForm):
    lemail = StringField('E-mail', validators=[DataRequired(), Email()])
    lsenha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso', default=True)
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    bg_perfil_img = FileField('Background do Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    bg_perfil_url = StringField('Background do Perfil URL')

    curso_excel = lembrar_dados = BooleanField('Execel Impressionador', default=False)
    curso_powerbi = lembrar_dados = BooleanField('PowerBi Impressionador', default=False)
    curso_python = lembrar_dados = BooleanField('Python Impressionador', default=False)
    curso_vba = lembrar_dados = BooleanField('VBA Impressionador', default=False)
    curso_ppt = lembrar_dados = BooleanField('Apresentações Impressionador', default=False)
    curso_sql = lembrar_dados = BooleanField('SQL Impressionador', default=False)

    botao_submit_editarperfil = SubmitField('Salvar')

    def validate_email(self, email):
    	
    	if current_user.email != email.data:
            usuario = Usuarios.query.filter_by(email=email.data).first()
            
            if usuario:
                raise ValidationError(f'"{email.data}" não esta disponivel.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Texto do Post', validators=[DataRequired()])
    botao_submit = SubmitField('Publicar')

