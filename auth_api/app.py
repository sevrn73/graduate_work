from datetime import timedelta

from flask import Flask, request, send_from_directory
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from src.api.v1.admin import create_admin_role
from src.api.v1.api_v1_blueprint import app_v1_blueprint
from src.cache.redis_cache import redis_cache
from src.core.config import jaeger_settings, project_settings, redis_settings
from src.core.tracer import configure_tracer
from src.db.db import init_db
from src.db.roles_service import get_user_primary_role


SWAGGER_URL = "/auth_api/docs/"
API_URL = "/auth_api/static/swagger_config.yaml"
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
limiter = Limiter(key_func=get_remote_address, default_limits=["300 per day", "60 per hour"])


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = project_settings.SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=redis_settings.ACCESS_EXPIRES_IN_SECONDS)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=redis_settings.REFRESH_EXPIRES_IN_SECONDS)
    app.config["RATELIMIT_STORAGE_URL"] = redis_settings.RATELIMIT_STORAGE_URL
    limiter.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        """
        Callback function to check if a JWT exists in the redis blocklist
        """
        jti = jwt_payload["jti"]
        token_in_redis = redis_cache._get(jti)
        return token_in_redis is not None

    @jwt.additional_claims_loader
    def add_roles_to_access_token(identity):
        return get_user_primary_role(identity)

    app.register_blueprint(swagger_blueprint)
    app.register_blueprint(app_v1_blueprint, url_prefix="/v1")
    app.cli.add_command(create_admin_role)

    @app.route("/auth_api/static/<path:path>")
    def send_static(path):
        return send_from_directory("static", path)

    if jaeger_settings.ENABLE_TRACER:
        configure_tracer()
    FlaskInstrumentor().instrument_app(app)

    @app.before_request
    def before_request():
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            raise RuntimeError("Request id is required")

    return app


def start_app():
    app = create_app()
    init_db(app)
    app.app_context().push()
    return app


if __name__ == "__main__":
    start_app()
