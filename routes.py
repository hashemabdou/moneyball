from flask import render_template, url_for, redirect, flash, request
from app import app, db
from models import User, Game, Pick, Round
from forms import RegistrationForm, LoginForm, NewRoundForm, GameForm, GamesForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/home')
def home():
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
            # Check if the user is an admin and redirect to admin_home if true
            if user.is_admin:
                return redirect(url_for('admin_home'))
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
    current_round = Round.query.filter_by(is_active=True).first()
    previous_performance = None  # Initialize to a default value
    total_winnings = None        # Initialize to a default value
    progress_this_round = None   # Initialize to a default value

    if current_round:
        current_picks = Pick.query.filter_by(user_id=current_user.id, round=current_round.id).all()

        # Calculate previous round performance (this is a placeholder logic)
        previous_round = Round.query.filter(Round.id < current_round.id).order_by(Round.id.desc()).first()
        previous_picks = Pick.query.filter_by(user_id=current_user.id, round=previous_round.id).all()
        previous_performance = "Your performance details here"  # Replace with actual logic

        # Calculate total all-time winnings (this is a placeholder logic)
        total_winnings = "Your winnings calculation here"  # Replace with actual logic

        # Calculate progress in the current round (this is a placeholder logic)
        progress_this_round = "Your progress calculation here"  # Replace with actual logic

    else:
        current_picks = []
    return render_template('user_home.html', current_picks=current_picks, previous_performance=previous_performance, total_winnings=total_winnings, progress_this_round=progress_this_round)

@app.route('/admin_home')
@login_required
def admin_home():
    if not current_user.is_admin:
        return redirect(url_for('home'))

    # Fetch all active rounds
    active_rounds = Round.query.filter_by(is_active=True).all()

    # Fetch all games and picks for admin overview (if needed)
    all_games = Game.query.all()
    all_picks = Pick.query.all()

    return render_template('admin_home.html', active_rounds=active_rounds, all_games=all_games, all_picks=all_picks)



@app.route('/new_round', methods=['GET', 'POST'])
@login_required
def new_round():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = NewRoundForm()
    if form.validate_on_submit():
        new_round = Round(name=form.name.data, is_active=True)
        db.session.add(new_round)
        db.session.commit()
        flash('New round created!', 'success')
        return redirect(url_for('admin_home'))
    return render_template('new_round.html', form=form)

# routes.py
@app.route('/manage_round/<int:round_id>', methods=['GET', 'POST'])
@login_required
def manage_round(round_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))

    round = Round.query.get_or_404(round_id)
    form = GamesForm()
    
    if form.validate_on_submit():
        for game_form in form.games:
            new_game = Game(
                round_id=round.id,
                home_team=game_form.home_team.data,
                away_team=game_form.away_team.data,
                game_date=game_form.game_date.data
            )
            db.session.add(new_game)
        db.session.commit()
        flash('Games added to the round!', 'success')

    # Fetch games for the current round
    games_in_round = Game.query.filter_by(round_id=round_id).all()

    return render_template('manage_round.html', round=round, form=form, games_in_round=games_in_round)



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