from flask import (
    Blueprint,
    render_template,
    request,
)

from app.models import Transaction
from app.helpers import usd

transactions = Blueprint('transactions', __name__)


@transactions.route("/transactions")
def paginated():
    page = request.args.get('page', default=1, type=int)
    transactions_list = Transaction.query.paginate(per_page=3, page=page)
    return render_template("transactions.html", usd=usd, transactions=transactions_list)