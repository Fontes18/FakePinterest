# criar os formulários do nosso site
from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from FakePinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Usuário inexistente, crie uma conta")

class FormCriarLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Digite o nome do seu usuário", validators=[DataRequired()])
    senha = PasswordField("Digite uma senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Digite novamente a senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao =SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")
        
class FormFoto(FlaskForm):
    foto = FileField("foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")