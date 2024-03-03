from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    debug = bool(app.config['DEBUG'] == 'True')
    app.run(debug=debug)
