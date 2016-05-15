from flask.ext.wtf import Form
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class AddVacancyForm(Form):
    first_day = DateField('Prima zi', format='%m/%d/%Y')
    last_day = DateField('Ultima zi', format='%m/%d/%Y')
    submit = SubmitField('Salveaza')
