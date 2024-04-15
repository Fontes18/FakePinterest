# criar rotas do nosso site
from flask import render_template, url_for, redirect
from FakePinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from FakePinterest.forms import FormLogin, FormCriarLogin, FormFoto
from FakePinterest.models import Usuario, Post
import os
from werkzeug.utils import secure_filename

@app.route("/", methods =["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password,formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("homepage.html", form = formlogin)

@app.route("/criar-conta", methods =["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarLogin()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username = formcriarconta.username.data, 
                          password = senha, 
                          email = formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember = True)
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("/criar_conta.html", form = formcriarconta)

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuario está vendo o próprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o aquivo no photos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # Registrar este arquivo no banco de dados
            photo = Post(imagem=nome_seguro,id_usuario=current_user.id )
            database.session.add(photo)
            database.session.commit()
        return render_template("users.html", usuario=current_user, form=form_foto)

    else:
        usuario = Usuario.query.get(int(id_usuario))
    return render_template("users.html", usuario = usuario, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
def Feed():
    fotos = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template("Feed.html", fotos=fotos)