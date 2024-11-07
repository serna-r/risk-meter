from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms import widgets

data_list = ['Nickname', 'Name', 'Surname', 'birth date', 'gender', 'Profile photo', 'email', 'tlf', 'nacionality', 'location', 'address', 'Photos', 'Messages', 'subscription', 'purchases', 'money stored', 'key to other accounts', 'Sexual preferences']

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RiskForm(FlaskForm):
    # Authentication practices
    min_length = IntegerField('Minimum length', validators=[DataRequired()])
    min_mask = StringField('Minimum mask', validators=[DataRequired()])
    extra_sec = BooleanField('Extra security')
    two_factor = BooleanField('Two factor authentication')
    sign_in_method = StringField('Sign in method', validators=[DataRequired()])

    # Risk of data exposure
    risk_data_exp = MultiCheckboxField('Select the data collected', choices=data_list)

    # Risk appetite
    risk_appetite = IntegerField('Risk appetite 7-I do not care, 4-standard, 1-No way anything happens ', validators=[DataRequired()])

    # Password
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')