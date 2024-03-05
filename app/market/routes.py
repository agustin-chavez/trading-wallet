from flask import (
    Blueprint,
    render_template,
    request,
)

from app.tickers.model import Ticker
from app.utils.numbers_formatter import usd, volume
from app.utils.login_required_decorator import login_required

market = Blueprint('market', __name__)


@market.route("/market")
@login_required
def paginated():
    page = request.args.get('page', default=1, type=int)
    tickers = Ticker.query.paginate(per_page=5, page=page)
    return render_template("market.html", usd=usd, volume=volume, tickers=tickers)