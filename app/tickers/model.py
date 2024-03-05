from app import db


class Ticker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String, nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Ticker('{self.symbol}', '{self.name}', '{self.stock}', '{self.price}')"
