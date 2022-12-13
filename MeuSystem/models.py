from datetime import datetime
from MeuSystem import app, database, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_usuario(id_usuario):
	return Usuarios.get(id_usuario)



class Usuarios(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    token = database.Column(database.String, nullable=False)
    refresh_token = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    senha = database.Column(database.String, nullable=False)

	

with app.app_context(): 
	#database.drop_all() 
	database.create_all()
	
	