from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class BaseAgencyForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    address = StringField('Address', validators=[DataRequired(), Length(1, 64)])


class AddAgencyForm(BaseAgencyForm):
    submit = SubmitField('Add agency')


class EditAgencyForm(BaseAgencyForm):
    update = SubmitField('Update agency')
    delete = SubmitField('Delete agency')


class AddCompanyForm(Form):
    cif = StringField('CIF', validators=[DataRequired(), Length(1, 64)])
    name = StringField('Nume', validators=[DataRequired(), Length(1, 64)])
    address = StringField('Adresa', validators=[DataRequired(), Length(1, 64)])
    city = StringField('Oras', validators=[DataRequired(), Length(1, 64)])
    state = StringField('Judet', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Telefon', validators=[DataRequired(), Length(1, 64)])
    registration_id = StringField('Nr. de inregistrare', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Salveaza')
