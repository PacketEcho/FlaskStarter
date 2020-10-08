from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from loguru import logger


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = 'Guest'
        self.avatar_url = 'https://i.pravatar.cc/50'
        self.active = 0


login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.anonymous_user = Anonymous

db = SQLAlchemy()
logger.add('app.log', format="{time} {level} {message}", colorize=True)
