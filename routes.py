from flask import render_template, url_for, redirect, flash
from app import app, db
from models import User, Game, Pick
from forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_home'))
    elif current_user.is_authenticated:
        return redirect(url_for('user_home'))
    else:
        return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user and add to the database
        pass
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        # Authenticate the user and log them in
        pass
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user_home')
@login_required
def user_home():
    # Display user-specific home page
    pass

@app.route('/admin_home')
@login_required
def admin_home():
    # Display admin-specific home page
    pass

# Additional routes for admin actions, user actions, and displaying the leaderboard will be added here.