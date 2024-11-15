from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, NoneOf
from wtforms import widgets
import json

# Get the json with the choices
json_file_path = './flaskr/json/choices.json'
with open(json_file_path, 'r') as f: 
    JSON_CHOICES = json.load(f)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RiskForm(FlaskForm):
    # Authentication practices
    min_length = IntegerField('Minimum length', validators=[DataRequired()])
    min_mask = SelectField('Minimum mask', choices=[(x,x) for x in JSON_CHOICES["min_mask"]],validators=[DataRequired(), NoneOf(["Choose one"], message="You have to choose one")])
    extra_sec = BooleanField('Extra security')
    two_factor = BooleanField('Two factor authentication')
    sign_in_method = SelectField('Sign in method',choices=[(x,x) for x in JSON_CHOICES["sign_in_method"]], validators=[DataRequired(), NoneOf(["Choose one"], message="You have to choose one")])

    # Risk of data exposure
    risk_data_exp = MultiCheckboxField('Select the data collected', choices=JSON_CHOICES["risk_data_exp"])

    # Risk appetite
    risk_appetite = SelectField('Risk appetite', choices=[(x,x) for x in JSON_CHOICES["risk_appetite"]],validators=[DataRequired(), NoneOf(["Choose one"], message="You have to choose one")])

    # Submit
    submit = SubmitField('Submit')