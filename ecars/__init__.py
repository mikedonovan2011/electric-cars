from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from ecars.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'    # function name of our route for when login fails
login_manager.refresh_view = 'users.login'  # or when they logged in from a cookie but we want a fresh login
login_manager.login_message_category = 'info'
login_manager.needs_refresh_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Bootstrap(app)
    moment = Moment(app)

    from ecars.users.routes import users
    from ecars.posts.routes import posts
    from ecars.main.routes import main
    from ecars.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
