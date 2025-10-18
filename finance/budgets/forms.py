from flask_wtf import FlaskForm
from wtforms import SelectField,FloatField,SubmitField
from wtforms.validators import DataRequired, NumberRange

class BudgetForm(FlaskForm):
    category = SelectField('Category', choices=[
        ("food", "Food"),
        ("rent", "Rent"),
        ("utilities", "Utilities"),
        ("entertainment", "Entertainment"),
        ('shopping','Shopping'),
        ("transport", "Transport"),
        ("savings", "Savings"),
        ("other", "Other")
    ],validators=[DataRequired()])

    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0")])

    submit = SubmitField("Save Budget!")
