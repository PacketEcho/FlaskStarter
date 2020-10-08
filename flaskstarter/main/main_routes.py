import pendulum

from flask import Blueprint, render_template

from flaskstarter.extensions import db, login_manager
from flaskstarter.user.models.user import User

blueprint = Blueprint('main', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    query = User.query.filter_by(id=user_id)

    try:
        user = query.one()
    except Exception:
        return None
    else:
        user.last_login_on = pendulum.now()
        db.session.commit()
    return user


@blueprint.route('/')
def index():
    return render_template('main/index.html')
