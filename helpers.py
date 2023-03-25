import sqlite3

from flask import redirect, render_template, request, session
from functools import wraps


def get_db():
    connection = sqlite3.connect("conlang.db")
    return connection


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
