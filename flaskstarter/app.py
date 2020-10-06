import os

from flask import Flask, render_template, url_for

from flaskstarter import config
from flaskstarter.extensions import db
from flaskstarter.main import main_routes

app_env = os.environ.get('APPLICATION_ENVIRONMENT') or 'production'


def create_app():
    app = Flask(__name__)

    if app_env == 'development':
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.ProductionConfig)

    register_extensions(app)
    register_blueprints(app)
    register_utils(app)
    register_errorhandlers(app)

    return app


def register_extensions(app):
    db.init_app(app)

    return None


def register_blueprints(app):
    app.register_blueprint(main_routes.blueprint)

    return None


def register_utils(app):
    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    return None


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template(f'{error_code}.html'), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
