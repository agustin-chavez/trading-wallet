from app import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    share_price = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.shares}', '{self.ticker}', '{self.shares}')"