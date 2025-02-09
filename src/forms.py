from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import ValidationError,DataRequired,Length,EqualTo,Email


class Persona(FlaskForm):

    username=StringField('username',validators=[
        DataRequired(),
        Length(min=5,max=20)
    ])

    email=EmailField('email',validators=[
        DataRequired(),
        Length(min=10,max=100),
        Email()
    ])

    image=StringField('image',validators=[
        DataRequired(),
        Length(max=255)
    ])

    password=PasswordField('password',validators=[
        DataRequired(),
        Length(min=5,max=20)
    ])

    confirm=PasswordField('confirm',validators=[
        DataRequired(),
        Length(min=5,max=20),
        EqualTo('password',message='Las contraseñas no coinciden')
    ])

    submit=SubmitField('Enviar')


class Inicar(FlaskForm):

    email=EmailField('email',validators=[
        DataRequired(),
        Length(min=10,max=100),
        Email()
    ])

    
    password=PasswordField('password',validators=[
        DataRequired(),
        Length(min=5,max=20)
    ])
