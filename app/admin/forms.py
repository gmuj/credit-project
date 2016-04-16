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