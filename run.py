from app import create_app, db
from app.utils.yahoo_finance import init_yf_snapshot

app = create_app()

with app.app_context():
    db.create_all()
    init_yf_snapshot()

if __name__ == "__main__":
    debug = bool(app.config['DEBUG'] == 'True')
    app.run(debug=debug)
