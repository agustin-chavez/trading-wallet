from flask import (
    Blueprint,
    render_template,
    request,
)

from app.holdings.model import Holding
from app.utils.numbers_formatter import usd

wallet = Blueprint('wallet', __name__)


@wallet.route("/wallet")
def dashboard():
    page = request.args.get('page', default=1, type=int)
    holdings = Holding.query.paginate(per_page=3, page=page)
    return render_template("wallet.html", usd=usd, holdings=holdings)
