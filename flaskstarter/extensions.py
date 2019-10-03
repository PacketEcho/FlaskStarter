from flask_sqlalchemy import SQLAlchemy
from loguru import logger

db = SQLAlchemy()
logger.add('app.log', format="{time} {level} {message}", colorize=True)
