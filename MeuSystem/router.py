from MeuSystem import app
from flask import render_template, redirect, url_for, request, flash
from MeuSystem.autent import Bd
from MeuSystem.forms import Login, Form_Os
from datetime import datetime

#pagina de login

@app.route("/login", methods=['GET', 'POST'])
def login():
	
	form = Login()
	
	if form.validate_on_submit():
		return redirect(url_for('home'))
	
	
	return render_template('login.html', form=form)


# pagina home
	
@app.route('/')
def home():
	
	return render_template('home.html')


# pagina mostrar

@app.route('/info/<pagina>')
def mostrar(pagina):
	
	return render_template('frame.html', pagina=pagina)


# paginas de servicos

@app.route('/servicos')
def servicos():
	form = Form_Os()
	
	return render_template('servicos.html', form=form)

	# servisos ativos
@app.route('/servicos/servicos-ativos')
def servicos_ativos():
	
	return  render_template('sec_servAT.html')

	# servicos baixados
@app.route('/servicos/servicos-baixados')
def servicos_baixados():
	
	return  render_template('sec_servBA.html')


	# servicos baixados
@app.route('/servicos/servicos-retornos')
def servicos_retornos():
	
	return  render_template('sec_retornos.html')

@app.route('/cientes')
def clientes():
	
	return  render_template('sec_clientes.html')
