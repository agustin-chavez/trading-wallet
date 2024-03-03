from app import create_app, db, bcrypt
from app.models import User, Post
from app.posts.data import posts

app = create_app()

with app.app_context():
    db.create_all()
    print('Posts:', Post.query.count())
    if Post.query.count() == 0:
        print("Creating posts...")
        for post_data in posts:
            author = User.query.filter_by(username=post_data['author']).first()

            if not author:
                username = post_data['author'].replace(' ', '.')
                email = f"{post_data['author'].lower().replace(' ', '.')}@example.com"
                hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')

                author = User(username=username, email=email, password=hashed_password)
                db.session.add(author)
                db.session.commit()

            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                date_posted=post_data['date_posted'],
                author=author
            )

            db.session.add(post)
            db.session.commit()

        print("DB populated!")

if __name__ == "__main__":
    debug = bool(app.config['DEBUG'] == 'True')
    app.run(debug=debug)
