from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request, redirect, url_for, flash,
)
from flask_login import current_user

from app.holdings.model import Holding
from app.utils.numbers_formatter import usd
from app.utils.login_required_decorator import login_required
from app.tickers.model import Ticker
from app.transactions.model import Transaction
from app.wallet.forms import SellForm
from app import db

wallet = Blueprint('wallet', __name__)


@wallet.route("/wallet", methods=['GET', 'POST'])
@login_required
def dashboard():
    holdings = Holding.query.filter_by(user_id=current_user.id).all()
    for holding in holdings:
        ticker = Ticker.query.filter_by(symbol=holding.ticker).first()
        holding.price = ticker.price
        holding.name = ticker.name
    cash = current_user.cash
    balance = cash + sum(holding.price for holding in holdings)
    return render_template("wallet.html", usd=usd, holdings=holdings, balance=balance, cash=cash)


@wallet.route("/sell", methods=['GET', 'POST'])
@login_required
def sell():
    symbol = request.args.get('symbol')
    if not symbol:
        return redirect(url_for('wallet.dashboard'))
    form = SellForm()
    ticker = Ticker.query.filter_by(symbol=symbol).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            stocks = int(form.stocks.data)
            fee = (stocks * ticker.price) * 4 / 100
            total_price = (stocks * ticker.price) - fee
            current_user.cash += total_price
            holding = Holding.query.filter_by(ticker=symbol).filter_by(user_id=current_user.id).first()
            if holding:
                if stocks > holding.shares:
                    flash(f"Invalid amount of stocks", "danger")
                    return render_template("sell.html", ticker=ticker, usd=usd, form=form)
                elif holding.shares == stocks:
                    db.session.delete(holding)
                else:
                    holding.shares -= stocks
            else:
                flash("No holdings were found in the wallet with that ticker", "danger")
                return redirect(url_for('wallet.dashboard'))
            transaction = Transaction(
                ticker=symbol,
                operation='SELL',
                shares=stocks,
                share_price=ticker.price,
                fee=fee,
                transaction_date=datetime.now(),
                user_id=current_user.id
            )
            db.session.add(transaction)
            db.session.commit()
            flash(f"Sold! {usd(total_price)} transferred to your wallet. Fee {usd(fee)}", "success")
            return redirect(url_for('wallet.dashboard'))
        else:
            flash(f"Invalid amount of stocks", "danger")
    return render_template("sell.html", ticker=ticker, usd=usd, form=form)
