from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database URI. 'site.db' is the name of the database file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize the Flask application with the configured database
db = SQLAlchemy(app)

# Define a model for the 'Technologies' table in the database
class Technology(db.Model):
    __tablename__ = 'technologies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


@app.route('/')
def home():
    technologies = Technology.query.all()
    return render_template('index.html', technologies=technologies)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all(Technology(**technology) for technology in  [
            {'id': 1, 'name': 'Python'},
            {'id': 2, 'name': 'Flask'},
            {'id': 3, 'name': 'SQLite3'},
            {'id': 4, 'name': 'Docker'},
        ])
        db.session.commit()

    app.run(host='0.0.0.0', debug=True, port=5001)