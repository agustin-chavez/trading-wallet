from flask import (
    Blueprint,
    render_template,
    request,
)

from app.models import Holding
from app.helpers import usd

wallet = Blueprint('wallet', __name__)


@wallet.route("/wallet")
def dashboard():
    page = request.args.get('page', default=1, type=int)
    holdings = Holding.query.paginate(per_page=3, page=page)
    return render_template("wallet.html", usd=usd, holdings=holdings)
