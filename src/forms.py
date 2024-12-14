from flask_wtf import Form, FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField, IntegerField

class TransactionForm(FlaskForm): 
    amount = IntegerField('amount')