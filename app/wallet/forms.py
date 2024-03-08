from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class SellForm(FlaskForm):
    stocks = IntegerField(
        default=1,
        validators=[
            DataRequired(),
            NumberRange(1, 999, "Please enter a valid quantity")
        ]
    )
    submit = SubmitField('Sell')

