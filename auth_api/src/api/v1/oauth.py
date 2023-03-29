from flask import Blueprint, jsonify, request
from src.db.account_service import add_record_to_login_history
from src.db.db_models import OAuthAccount, User
from src.db.oauth_service import create_user_oauth
from src.oauth.providers import OAuthSignIn

oauth = Blueprint("oauth_helper", __name__)


@oauth.route("/authorize/<provider>")
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@oauth.route("/oauth_callback/<provider>")
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    service_name = oauth.provider_name
    service_id = oauth.service_id

    account_model = OAuthAccount.query.filter_by(social_id=social_id).first()
    if account_model is None:
        email_exist = User.query.filter_by(email=email).first()
        if email_exist:
            email = None
        user_model = create_user_oauth(username, email, social_id, service_id, service_name)
    else:
        user_model = User.query.filter_by(id=account_model.user_id).first()

    add_record_to_login_history(user_model.id, request.user_agent.string)

    return oauth.create_tokens(identity=user_model.id)
