from flask import (
    Blueprint,
    render_template,
    request,
)

from app.models import Holding
from app.helpers import usd

market = Blueprint('market', __name__)


@market.route("/market")
def paginated():
    page = request.args.get('page', default=1, type=int)
    holdings = Holding.query.paginate(per_page=3, page=page)
    return render_template("market.html", usd=usd)