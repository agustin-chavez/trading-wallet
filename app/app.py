from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trading-wallet.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)