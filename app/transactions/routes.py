from flask import (
    Blueprint,
    render_template,
    request,
)

from app.transactions.model import Transaction
from app.utils.numbers_formatter import usd
from app.utils.login_required_decorator import login_required

transactions = Blueprint('transactions', __name__)


@transactions.route("/transactions")
@login_required
def paginated():
    page = request.args.get('page', default=1, type=int)
    transactions_list = Transaction.query.paginate(per_page=3, page=page)
    return render_template("transactions.html", usd=usd, transactions=transactions_list)