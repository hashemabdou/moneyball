from flask import render_template, url_for, redirect, flash, request
from app import app, db
from models import User, Game, Pick, Round
from forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

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
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user_home')
@login_required
def user_home():
    # Fetch user's current picks for the ongoing round
    current_round = Round.query.filter_by(is_active=True).first()
    current_picks = Pick.query.filter_by(user_id=current_user.id, round=current_round.id).all()

    # Calculate previous round performance (this is a placeholder logic)
    previous_round = Round.query.filter(Round.id < current_round.id).order_by(Round.id.desc()).first()
    previous_picks = Pick.query.filter_by(user_id=current_user.id, round=previous_round.id).all()
    previous_performance = "Your performance details here"  # Replace with actual logic

    # Calculate total all-time winnings (this is a placeholder logic)
    total_winnings = "Your winnings calculation here"  # Replace with actual logic

    # Calculate progress in the current round (this is a placeholder logic)
    progress_this_round = "Your progress calculation here"  # Replace with actual logic

    return render_template('user_home.html', current_picks=current_picks, previous_performance=previous_performance, total_winnings=total_winnings, progress_this_round=progress_this_round)

@app.route('/admin_home')
@login_required
def admin_home():
    if not current_user.is_admin:
        return redirect(url_for('home'))

    # Fetch all games and picks for admin overview
    all_games = Game.query.all()
    all_picks = Pick.query.all()

    # Fetch current round information
    current_round = Round.query.filter_by(is_active=True).first()

    return render_template('admin_home.html', all_games=all_games, all_picks=all_picks, current_round=current_round)


# Additional routes for admin actions, user actions, and displaying the leaderboard will be added here.

@app.route('/new_round', methods=['GET', 'POST'])
@login_required
def new_round():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = NewRoundForm()
    if form.validate_on_submit():
        new_round = Round(number=form.round_number.data, start_date=form.start_date.data, end_date=form.end_date.data)
        db.session.add(new_round)
        db.session.commit()
        flash('New round created!', 'success')
        return redirect(url_for('admin_home'))
    return render_template('new_round.html', form=form)

@app.route('/leaderboard')
def leaderboard():
    # Example query, adjust as needed
    winners = User.query.filter(User.picks.any(status='Winner')).all()
    return render_template('leaderboard.html', winners=winners)

@app.route('/make_pick', methods=['GET', 'POST'])
@login_required
def make_pick():
    form = PickForm()
    # Query available games and set choices
    available_games = [(game.id, f"{game.home_team} vs {game.away_team}") for game in Game.query.all()]
    form.set_choices(available_games)

    if form.validate_on_submit():
        # Example logic, adjust as needed
        new_pick = Pick(team=form.team.data, user_id=current_user.id, round=current_round, status='Active')
        db.session.add(new_pick)
        db.session.commit()
        flash('Pick submitted!', 'success')
        return redirect(url_for('user_home'))
    return render_template('make_pick.html', form=form)

@app.route('/round_summary')
@login_required
def round_summary():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    # Example logic, adjust as needed
    summary = generate_round_summary(current_round)
    return render_template('round_summary.html', summary=summary)