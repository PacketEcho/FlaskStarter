import json
import requests

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
from requests.exceptions import HTTPError, Timeout

from flaskstarter.config import Config
from flaskstarter.extensions import db
from flaskstarter.user.models.user import User, OAuth

blueprint = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')

client = WebApplicationClient(Config.GOOGLE_OAUTH_CLIENT_ID)
REQUEST_TIMEOUT = 300


def get_google_provider_cfg():
    with requests.Session() as session:
        try:
            response = session.get(Config.GOOGLE_DISCOVERY_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except Timeout as err:
            flash(f'The request timed out: {err}', category='error')
            return False
        except HTTPError as err:
            flash(f'HTTP error occurred: {err}', category='error')
            return False
        except Exception as err:
            flash(f'Other error occurred: {err}', category='error')
            return False

        if response.status_code == requests.codes.ok:
            result = response.json()
            return result
        else:
            return False


@blueprint.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)


@blueprint.route('/login/callback')
def callback():
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    with requests.Session() as session:
        try:
            response = session.post(token_url,
                                    headers=headers,
                                    data=body,
                                    auth=(Config.GOOGLE_OAUTH_CLIENT_ID,
                                          Config.GOOGLE_OAUTH_CLIENT_SECRET),
                                    timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except Timeout as err:
            flash(f'The request timed out: {err}', category='error')
            return False
        except HTTPError as err:
            flash(f'HTTP error occurred: {err}', category='error')
            return False
        except Exception as err:
            flash(f'Other error occurred: {err}', category='error')
            return False

        if response.status_code == requests.codes.ok:
            token_json = response.json()
        else:
            return False

    client.parse_request_body_response(json.dumps(token_json))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)

    with requests.Session() as session:
        try:
            response = session.get(uri, headers=headers, data=body, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except Timeout as err:
            flash(f'The request timed out: {err}', category='error')
            return False
        except HTTPError as err:
            flash(f'HTTP error occurred: {err}', category='error')
            return False
        except Exception as err:
            flash(f'Other error occurred: {err}', category='error')
            return False

        if response.status_code == requests.codes.ok:
            userinfo = response.json()
        else:
            return False

    if userinfo['email_verified']:
        user_id = userinfo['sub']
        email = userinfo['email']
        avatar = userinfo['picture']
        username = userinfo['name']
        first_name = userinfo['given_name']
        last_name = userinfo['family_name']
    else:
        return 'User email not available or not verified by Google', 400

    query = OAuth.query.filter_by(provider_user_id=user_id)
    oauth = query.first()
    if not oauth:
        oauth = OAuth(provider='google', provider_user_id=user_id)

    if oauth.user:
        login_user(oauth.user)
    else:
        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    avatar_url=avatar
                    )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user)

    return redirect(url_for('main.index'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@blueprint.route('/')
def index():
    return render_template('user/login.html')
