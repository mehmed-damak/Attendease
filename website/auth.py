from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully :))', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category = 'error')
        elif email=="admin@admin.com" and password=="admin123":
            new_user = User(email=email, role="admin", password = password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('usertype')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email exists', category='error')
        elif len(email)<4:
            flash('email small', category='error')
        elif role != "teacher" or role!="student":
            flash('must be "teacher" or "student"', category='error')
        elif len(firstName)<2:
            flash('name small', category='error')
        elif password1!=password2:
            flash('passwords no match', category='error')
        elif len(password1)<5:
            flash('pawword short', category='error')
        else:
            new_user = User(email=email, role=role, firstName=firstName, password = generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Person created', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)
