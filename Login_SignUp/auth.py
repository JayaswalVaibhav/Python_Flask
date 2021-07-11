from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if request method is POST, check the credentials
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # query the database with email
        user = User.query.filter_by(email=email).first()

        # if user is not present, flash the error
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for('auth.login'))
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # query the database with email
        user = User.query.filter_by(email=email).first()

        # if user is present, redirect user to sign up page and flash a message
        if user:
            flash("Email is already registered. Please try with a different email.")
            return redirect(url_for('auth.signup'))

        # create new user if user is not present in the database
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add user to database
        db.session.add(new_user)
        db.session.commit()
        # redirect the user to login page
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    # login is required to use logout, therefore login_required from flask_login is used
    logout_user()
    return redirect(url_for('auth.login'))

