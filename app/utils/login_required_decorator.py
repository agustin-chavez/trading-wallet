from functools import wraps

from flask import request, redirect, url_for
from flask_login import current_user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('users.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
