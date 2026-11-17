import logging
from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.secret_key = 'chave_super_secreta_padaria_spolbp1'

    # Configuração básica de logs
    logging.basicConfig(level=logging.INFO)

    # Registro de Blueprints
    from app.controllers.auth_bp import auth_bp
    from app.controllers.padaria_bp import padaria_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(padaria_bp)

    # Tratamento de erro 404
    @app.errorhandler(404)
    def pagina_nao_encontrada(error):
        app.logger.warning(f"Página não encontrada (404): {error}")
        return render_template('404.html'), 404

    return app