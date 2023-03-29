import json
from enum import Enum
from typing import List

from flask import Response, current_app, jsonify, redirect, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from rauth import OAuth2Service


# class syntax
class ProviderNames(Enum):
    Yandex = "yandex"
    Google = "google"


class OAuthSignIn:
    providers = None

    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        credentials = current_app.config["OAUTH_CREDENTIALS"][provider_name]
        self.consumer_id = credentials["id"]
        self.consumer_secret = credentials["secret"]

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self) -> str:
        return url_for("oauth_helper.oauth_callback", provider=self.provider_name, _external=True)

    def create_tokens(self, identity: str) -> Response:
        access_token = create_access_token(identity=identity, additional_claims={"is_administrator": False})
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def get_provider(self, provider_name: str) -> str:
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__(ProviderNames.Yandex.value)
        self.service = OAuth2Service(
            name=ProviderNames.Yandex.value,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.yandex.ru/authorize",
            access_token_url="https://oauth.yandex.ru/token",
            base_url="https://oauth.yandex.ru",
        )
        self.service_id = "01"

    def authorize(self) -> Response:
        return redirect(
            self.service.get_authorize_url(
                scope="login:email login:info",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self) -> List[str]:
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                "code": request.args["code"],
                "response_type": "code",
                "grant_type": "authorization_code",
                "redirect_uri": self.get_callback_url(),
            },
            decoder=decode_json,
        )
        info = oauth_session.get(url="https://login.yandex.ru/info").json()
        social_id = info.get("id")
        login = info.get("login")
        email = info.get("default_email")
        return social_id, login, email


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__(ProviderNames.Google.value)
        self.service = OAuth2Service(
            name=ProviderNames.Google.value,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            access_token_url="https://oauth2.googleapis.com/token",
            base_url="https://www.googleapis.com/",
        )
        self.service_id = "02"

    def authorize(self) -> Response:
        return redirect(
            self.service.get_authorize_url(
                scope="email",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self) -> List[str]:
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                "code": request.args["code"],
                "grant_type": "authorization_code",
                "redirect_uri": self.get_callback_url(),
            },
            decoder=decode_json,
        )
        me = oauth_session.get("oauth2/v2/userinfo").json()
        return f"{ProviderNames.Google.value}$" + me["id"], me.get("email").split("@")[0], me.get("email")
