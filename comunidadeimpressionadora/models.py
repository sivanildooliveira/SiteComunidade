from comunidadeimpressionadora import app, database, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import url_for


@login_manager.user_loader
def load_usuario(id_usuario):
	return Usuarios.query.get(int(id_usuario))

class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    bg_perfil = database.Column(database.String, default='e186eb6deeae0c65db343938923d8f790099ecff3afe3c5f.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='não informado')


    def retur_foto_perfil(self):
        return url_for('static', filename=f'fotos_perfil/{self.foto_perfil}')

    
    def atualizar_cursos(self, form):
        lista_curso = []
        for campo in form:
            if "curso_" in campo.name:
                if campo.data:
                    lista_curso.append(campo.label.text)
        self.cursos = ";".join(lista_curso)
        


    def quant_cursos(self):
        if self.cursos in ("não informado", ""):
            quant = 0
        else:
            quant = len(self.cursos.split(";"))
        return quant
    

    def quant_posts(self):
        return len(self.posts)


    


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)



    def data_hora_post(self):
        return self.data_criacao.strftime("%d/%m/%Y")



with app.app_context():

    #database.drop_all()
    database.create_all()

    pass