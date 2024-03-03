from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class HoldingForm(FlaskForm):
    symbol = StringField(
        'Symbol',
        validators=[
            DataRequired()
        ]
    )

    shares = IntegerField(
        'Shares',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Holding')