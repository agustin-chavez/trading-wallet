from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request, redirect, url_for, flash,
)
from flask_login import current_user

from app.tickers.model import Ticker
from app.utils.numbers_formatter import usd, volume
from app.utils.login_required_decorator import login_required
from app.market.forms import BuyForm
from app.holdings.model import Holding
from app import db
from app.transactions.model import Transaction

market = Blueprint('market', __name__)


@market.route("/market")
@login_required
def paginated():
    page = request.args.get('page', default=1, type=int)
    tickers = Ticker.query.paginate(per_page=5, page=page)
    cash = current_user.cash
    return render_template("market.html", usd=usd, volume=volume, tickers=tickers, cash=cash)


@market.route("/buy", methods=['GET', 'POST'])
@login_required
def buy():
    symbol = request.args.get('symbol')
    if not symbol:
        return redirect(url_for('market.paginated'))
    form = BuyForm()
    ticker = Ticker.query.filter_by(symbol=symbol).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            stocks = int(form.stocks.data)
            fee = (stocks * ticker.price) * 4 / 100
            total_price = (stocks * ticker.price) + fee
            if current_user.cash > total_price:
                current_user.cash -= total_price
                holding = Holding.query.filter_by(ticker=symbol).filter_by(user_id=current_user.id).first()
                if holding:
                    holding.shares += stocks
                else:
                    holding = Holding(ticker=symbol, shares=stocks, user_id=current_user.id)
                    db.session.add(holding)
                transaction = Transaction(
                    ticker=symbol,
                    operation='BUY',
                    shares=stocks,
                    share_price=ticker.price,
                    fee=fee,
                    transaction_date=datetime.now(),
                    user_id=current_user.id
                )
                db.session.add(transaction)
                db.session.commit()
                flash(f"Bought! {symbol} is now on your holdings", "success")
                return redirect(url_for('wallet.dashboard'))
            else:
                flash(
                    f"The total price for {stocks} stocks is {usd(total_price)}. Not enough cash: {usd(current_user.cash)}", "danger")
        else:
            flash(f"Invalid amount of stocks", "danger")
    return render_template("buy.html", ticker=ticker, usd=usd, form=form)
