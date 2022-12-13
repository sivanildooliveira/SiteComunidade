from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


database = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = '29cecf8afd6176f56bb3f5o472d390d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SistemRet.db'

database.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "login"



from MeuSystem import router