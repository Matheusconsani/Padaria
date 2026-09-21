from datetime import timedelta
from flask import Flask
from app.middlewares.auth import verificar_sessao


def create_app():
    app = Flask(__name__)
    app.secret_key = "chave_super_secreta_padaria"

    # Define que sessões permanentes expiram em 3 horas
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=3)

    from app.controllers.admin_bp import admin_bp
    from app.controllers.loja_bp import loja_bp

    app.register_blueprint(loja_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    app.before_request(verificar_sessao)

    return app