
from enum import auto
from fileinput import filename
from re import S
from turtle import pos
from flask import render_template, redirect, url_for, request, flash, abort
from comunidadeimpressionadora import app, database#, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.functionss import salvar_imagem
from comunidadeimpressionadora.models import Usuarios, Post
from flask_login import login_user, logout_user, current_user, login_required
from comunidadeimpressionadora.functionss import salvar_imagem, salvar_bg_imagem

@app.route('/')
@login_required
def home():
    posts = Post.query.order_by(Post.id.desc())
    
    return render_template('home.html', posts=posts)
 

@app.route('/contato')
@login_required
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuarios.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuarios.query.filter_by(email=form_login.lemail.data).first()     
        if usuario and  form_login.lsenha.data == usuario.senha:#bcrypt.check_password_hash(usuario.senha, form_login.lsenha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)        
            flash(f'Você esta logado!', 'alert-success')        
            par_next = request.args.get('next')
            print(par_next)
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))       	 
        else:
            flash(f'Falha no login! E-mail ou Senha são Inválidos. Tente novamente.', 'alert-danger')
            


    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        par_next = request.args.get('next')
        #criar usuario
        senha_criptografada = form_criarconta.senha.data#bcrypt.generate_password_hash(form_criarconta.senha.data)
        print(senha_criptografada)
        usuario = Usuarios(username=form_criarconta.username.data.title(), email=form_criarconta.email.data, senha=senha_criptografada)
        #adicionar usuario a sessao
        database.session.add(usuario)
        #comitar no banco de dados
        database.session.commit()
        
        usuario = Usuarios.query.filter_by(email=form_criarconta.email.data).first()
        login_user(usuario)
        flash(f'Bem Vindo {current_user.username}!', 'alert-success')

        if par_next:
            return redirect(par_next)
        else:
            return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)
    

@app.route('/sair')
def sair():
	logout_user()
	flash('Você não esta Logado!', 'alert-warning')
	return redirect(url_for('home'))



@app.route('/perfil')
@login_required
def perfil():
    editor = False
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    bg_perfil = url_for('static', filename=f'bg_perfil/{current_user.bg_perfil}') if  'https://' not in current_user.bg_perfil else current_user.bg_perfil

    return render_template('perfil.html', foto_perfil=foto_perfil, bg_perfil=bg_perfil, editor=editor, len=len)







@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    editor = True
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data.title()
        current_user.email = form.email.data

        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            if nome_imagem:
                current_user.foto_perfil = nome_imagem
            else:
                flash("Erro ao Salvar Foto de Perfil tente uma imagem JPG, JPEG, PNG, WEBP", 'alert-danger')
        if form.bg_perfil_url.data:
            nome_imagem = form.bg_perfil_url.data
            current_user.bg_perfil = nome_imagem
                
        if form.bg_perfil_img.data:
            nome_imagem = salvar_bg_imagem(form.bg_perfil_img.data)
            current_user.bg_perfil = nome_imagem

        current_user.atualizar_cursos(form)
        database.session.commit()
        flash('Perfil Alterado com Sucesso!', 'alert-success')
        return redirect(url_for('perfil'))

    form.username.data = current_user.username
    form.email.data = current_user.email
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    bg_perfil = url_for('static', filename=f'bg_perfil/{current_user.bg_perfil}') if  'https://' not in current_user.bg_perfil else current_user.bg_perfil

    return render_template('editarperfil.html', form=form,  foto_perfil=foto_perfil, bg_perfil=bg_perfil, editor=editor)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso", "alert-success")
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

@app.route('/post/<id_post>&<pg>', methods=['GET', 'POST'])
@login_required
def exibir_post(id_post, pg='home'):
    form = FormCriarPost()
    post = Post.query.get(id_post)
    global pagina 
    pagina = pg

    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        database.session.commit()
        flash("Atualização salva com sucesso!", "alert-success")
    if current_user == post.autor:
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
        return render_template('exibir_post.html', post=post, form=form)
    else:
        return render_template('exibir_post.html', post=post)


@app.route('/post/<id_post>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(id_post):
    post = Post.query.get(id_post)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post Excluido", "alert-warning")
        return redirect(url_for(pagina))
    else:
        return abort(403)
