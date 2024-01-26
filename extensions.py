from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db) 
    
@login_manager.user_loader
def load_user(user_id):
    from models import User  # Import here to avoid circular dependency
    return User.query.get(int(user_id))