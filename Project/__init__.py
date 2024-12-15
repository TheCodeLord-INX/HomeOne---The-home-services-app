from datetime import timedelta, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
from .models import db, Services

def create_app():
    app.config['SECRET_KEY'] = 'thisismykey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 1)

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User, Services, ServiceRemarks

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            User.create_dummy_admin()
            User.create_dummy_professionals()
            User.create_dummy_user()
            Services.create_services()
            ServiceRemarks.create_service_remarks()
        except Exception as e:
            print(e)
    return app