from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, abort
from app.holdings.forms import HoldingForm
from app.models import Holding
from app import db
from flask_login import current_user, login_required

holdings = Blueprint('holdings', __name__)


@holdings.route("/holding/buy", methods=['POST', 'GET'])
@login_required
def buy():
    form = HoldingForm()
    if form.validate_on_submit():
        holding = Holding(title=form.symbol.data, content=form.shares.data, user=current_user)
        db.session.add(holding)
        db.session.commit()
        flash("Your new holding is now in your investments portfolio!", "success")
        return redirect(url_for('main.home'))
    return render_template('holding.html', title='Buy', form=form, legend='Add a new holding to your portfolio')


@holdings.route("/holding/<int:holding_id>", methods=['POST', 'GET'])
def holding(holding_id):
    post = Holding.query.get_or_404(holding_id)
    return render_template('holding.html', title=holding.symbol, holding=holding)


@holdings.route("/holding/<int:holding_id>/sell", methods=['POST', 'GET'])
@login_required
def update_post(holding_id):
    post = Holding.query.get_or_404(holding_id)
    if post.author != current_user:
        abort(403)
    form = HoldingForm()
    if form.validate_on_submit():
        post.title = form.symbol.data
        post.content = form.shares.data
        db.session.commit()
        flash('Your holding has been updated', 'success')
        return redirect(url_for('holdings.holding', holding_id=holding.id))
    elif request.method == 'GET':
        form.symbol.data = holding.symbol
        form.shares.data = holding.shares
    form.symbol.data = holding.symbol
    form.shares.data = holding.shares
    return render_template('holding.html', title='Update Holding', form=form, legend='Update Holding')

