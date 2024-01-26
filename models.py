from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    picks = db.relationship('Pick', backref='user', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))  # Foreign key
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    game_date = db.Column(db.DateTime, nullable=False)
    picks = db.relationship('Pick', backref='game', lazy=True)

class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(100), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Alive, Eliminated, Winner

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    games = db.relationship('Game', backref='round', lazy=True)
    is_active = db.Column(db.Boolean, default=True)