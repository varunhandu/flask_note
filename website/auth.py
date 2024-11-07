from flask import Blueprint, request, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='error')
        else:
            flash("this user does not exist", category='error')
    return render_template("login.html", user=current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('logged out', category='success')
    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password1')
        confirmation = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists", category='error')
        elif(password != confirmation):
            flash("Passwords do not match", category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for("views.home"))
    return render_template("signup.html", user=current_user)
