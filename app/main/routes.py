from flask import Blueprint
from flask import render_template, request

from app.models import Holding

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', default=1, type=int)
    holdings = Holding.query.paginate(per_page=3, page=page)
    return render_template("home.html", holdings=holdings)

