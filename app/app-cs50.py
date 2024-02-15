import os
import re

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from app.helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    try:
        user_id = session["user_id"]

        result = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if not result:
            flash("There was an unexpected error trying to get user information.", "error")
            return redirect("/logout")

        user = result[0]
        cash = user["cash"]

        holdings = db.execute("SELECT * FROM holdings WHERE user_id = ?", user_id)

        if not holdings:
            flash("Looks like you don't own any stocks yet...")

        total = cash + sum(holding["price"] for holding in holdings)

        return render_template("index.html", holdings=holdings, cash=usd(cash), total=usd(total), usd=usd)
    except Exception as e:
        print("[INDEX] Error: ", e)
        return apology("An unexpected error occurred", 500)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    try:
        user_id = session["user_id"]

        if request.method == "POST":

            symbol = request.form.get("symbol").upper()

            try:
                shares_to_buy = int(request.form.get("shares"))
            except:
                return apology("invalid shares amount", 400)

            if not symbol:
                return apology("must provide symbol", 400)
            elif shares_to_buy < 1:
                return apology("must provide shares", 400)

            quote = lookup(symbol)

            if not quote:
                return apology(f"no quote found for {symbol}", 400)

            total_price = quote["price"] * shares_to_buy

            result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

            if not result:
                flash("There was an unexpected error trying to get user information.", "error")
                return redirect("/logout")

            cash = result[0]["cash"]

            if (cash < total_price):
                return apology(f"no enough cash available for {shares_to_buy} shares of {symbol}", 412)

            holdings = db.execute("SELECT * FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol)
            holding = holdings[0] if holdings else None

            price = quote["price"]
            date = datetime.now()

            if holding:
                shares = shares_to_buy + holding.get("shares")
                db.execute("UPDATE holdings SET shares = ?, price = ?, bought_date = ? WHERE id = ?",
                           shares, price, date, holding["id"])
                flash(f"You successfully increased your holdings of {symbol} from {holding['shares']} to {shares}")
            else:
                print("Executing insert in db")
                db.execute("INSERT INTO holdings (user_id, symbol, shares, price, bought_date) VALUES (?, ?, ?, ?, ?)",
                           user_id, symbol, shares_to_buy, price, date)
                flash(f"You have acquired {shares_to_buy} shares of {symbol} successfully!")

            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)

            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transaction_date) VALUES (?, ?, ?, ?, ?)",
                       user_id, symbol, shares_to_buy, total_price, date)

            return redirect("/")
        else:
            return render_template("buy.html")
    except Exception as e:
        print("[BUY] Error: ", e)
        return apology("An unexpected error occurred", 500)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    try:
        user_id = session["user_id"]
        transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
        return render_template("history.html", transactions=transactions, usd=usd)

    except Exception as e:
        print("[HISTORY] Error: ", e)
        return apology("An unexpected error occurred", 500)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    try:
        if request.method == "POST":

            symbol = request.form.get("symbol").upper()

            if not symbol or not re.search("[a-zA-Z]", symbol):
                return apology("must provide a valid symbol", 400)

            quote = lookup(symbol)

            if quote:
                return render_template("quoted.html", symbol=symbol, price=usd(quote["price"]))
            else:
                return apology("symbol not found", 400)
        else:
            return render_template("quote.html")
    except Exception as e:
        print("[QUOTE] Error: ", e)
        return apology("An unexpected error occurred", 500)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    try:
        if request.method == 'POST':
            if not request.form.get("username"):
                return apology("must provide username", 400)

            elif not request.form.get("password"):
                return apology("must provide password", 400)

            elif not request.form.get("confirmation"):
                return apology("must provide a confirmation for the password", 400)

            username = request.form.get("username")
            password = request.form.get("password")

            result = db.execute("SELECT id FROM users WHERE username = ?", username)
            username_already_exists = len(result) != 0

            if username_already_exists:
                return apology("the username was already taken", 400)
            elif password != request.form.get("confirmation"):
                return apology("the passwords doesn't match", 400)
            elif len(password) < 8:
                return apology("the password should have at least 8 characters", 400)
            elif not (re.search("[a-zA-Z]", password) and re.search("[0-9]", password) and re.search("[^a-zA-Z0-9\s]", password)):
                return apology("the password should have a combination of numbers, letters and special characters", 400)
            elif not re.fullmatch("[a-zA-Z0-9._-]*", username):
                return apology("the username can't have any special characters", 400)
            elif len(username) < 8 and len(username) > 12:
                return apology("the username should have between 8 and 12 characters", 400)
            else:
                hash = generate_password_hash(password)
                db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", username, hash, 10000)
                return redirect("/")

        else:
            return render_template("register.html")
    except Exception as e:
        print("[REGISTER] Error:", e)
        return apology("An unexpected error occurred", 500)


@ app.route("/sell", methods=["GET", "POST"])
@ login_required
def sell():
    """Sell shares of stock"""
    try:
        user_id = session["user_id"]

        if request.method == "POST":

            symbol = request.form.get("symbol")

            if not symbol:
                return apology("must provide a symbol", 400)

            symbol = symbol.upper()

            shares_to_sell = int(request.form.get("shares"))

            holdings = db.execute("SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol)

            if not holdings:
                return apology("symbol wasn't found in holdings", 400)

            holding = holdings[0]
            available_shares = holding["shares"]

            if not shares_to_sell or shares_to_sell > available_shares:
                return apology("not enough shares available to sell", 400)

            shares = available_shares - shares_to_sell

            if shares:
                db.execute("UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?", shares, user_id, symbol)
            else:
                db.execute("DELETE FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol)

            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
            cash_obtained = lookup(symbol)["price"] * shares_to_sell
            cash = cash + cash_obtained
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

            date = datetime.now()
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transaction_date) VALUES (?, ?, ?, ?, ?)",
                       user_id, symbol, shares_to_sell * -1, cash_obtained, date)

            flash(f"You have successfully sold {shares_to_sell} {symbol} shares")
            return redirect("/")

        else:
            holdings = db.execute("SELECT * FROM holdings WHERE user_id = ?", user_id)
            return render_template("sell.html", holdings=holdings)
    except Exception as e:
        print("[SELL] Error: ", e)
        return apology("An unexpected error occurred", 500)
