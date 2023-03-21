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

def validate_password(password):
    verification_status = True

    # If the password confirmation doesn't match the password
    if request.form.get("confirmation") != password:
        notification_error = "The passwords do not match"
        verification_status = False
        #return render_template("register.html", notification_error = notification_error)
        
    # If the password is too short
    elif len(password) < 8:
        notification_error = "The passwords needs to have minimum 8 characters"
        verification_status = False
        #return render_template("register.html", notification_error = notification_error)
    
    elif not any(char.isdigit() for char in password):
        notification_error = "The passwords needs to contain at least one number"
        verification_status = False
        #return render_template("register.html", notification_error = notification_error)
    
    return verification_status
