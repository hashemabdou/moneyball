from flask import Flask
from extensions import db, login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7agasereya'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moneyball.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'signin'  # Set the view for login (adjust as needed)

from models import User, Game, Pick

@app.cli.command('create-db')
def create_db():
    db.create_all()
    print('Database tables created.')

from routes import *

if __name__ == '__main__':
    app.run(debug=True)