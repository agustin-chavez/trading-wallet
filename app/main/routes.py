from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    request,
)

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")


@main.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
