from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Agency


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Parola', validators=[Required()])
    remember_me = BooleanField('Pastreaza-ma logat')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    name = StringField('Nume si prenume', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Username-ul poate contine doar caractere, '
                                          'cifre, punct sau undescore')])
    password = PasswordField('Parola', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirma parola', validators=[Required()])
    agency = SelectField('Agentia', validators=[Required()], coerce=int)
    submit = SubmitField('Inregistrare')

    def __init__(self):
        super(RegistrationForm, self).__init__()
        self.agency.choices = [(agency.id, agency.name)
                               for agency in Agency.query.order_by('name')]

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email-ul exista deja in baza de date.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username-ul exista deja in baza de date.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Parola veche', validators=[Required()])
    password = PasswordField('Parola noua', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirma noua parola', validators=[Required()])
    submit = SubmitField('Salveaza')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reseteaza parola')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Parola noua', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirma parola', validators=[Required()])
    submit = SubmitField('Reseteaza parola')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Nu am gasit adresa de email in baza de date.')


class ChangeEmailForm(Form):
    email = StringField('Email nou', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Parola', validators=[Required()])
    submit = SubmitField('Salveaza')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
