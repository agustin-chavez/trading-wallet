from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class SellForm(FlaskForm):
    stocks = IntegerField(
        default=1,
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField('Sell')

