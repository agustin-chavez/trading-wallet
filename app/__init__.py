from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.main.routes import main
    app.register_blueprint(main)

    from app.users.routes import users
    app.register_blueprint(users)

    from app.market.routes import market
    app.register_blueprint(market)

    from app.wallet.routes import wallet
    app.register_blueprint(wallet)

    from app.transactions.routes import transactions
    app.register_blueprint(transactions)

    from app.errors.handlers import errors
    app.register_blueprint(errors)

    return app
