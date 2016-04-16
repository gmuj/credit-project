from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length


class AgencyForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    address = StringField('Address', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Add agency')