from flask import Flask
from extensions import db, login_manager, migrate, init_extensions
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '7agasereya'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moneyball.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_extensions(app)

login_manager.login_view = 'signin'  # Set the view for login (adjust as needed)

from models import User, Game, Pick

@app.cli.command('create-db')
def create_db():
    db.create_all()
    print('Database tables created.')

@app.cli.command('create-admin')
def create_admin():
    """Create an admin user."""
    username = 'admin'
    email = 'admin@example.com'
    password = generate_password_hash('ilovehashem')

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        print('An admin user already exists.')
        return

    admin_user = User(username=username, email=email, password=password, is_admin=True)
    db.session.add(admin_user)
    db.session.commit()
    print('Admin user created.')

@app.context_processor
def context_processor():
    def is_active(route_name):
        if request.path == url_for(route_name):
            return 'active'  # This is the class name for active links
        return ''
    return dict(is_active=is_active)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)