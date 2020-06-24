import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from sistema.api.helpers.blacklist import BLACKLIST

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()


def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from sistema.api.resources.tarefa import tarefa_blueprint
    from sistema.api.resources.projeto import projeto_blueprint
    from sistema.api.resources.funcionario import funcionario_blueprint
    from sistema.api.resources.usuario import usuario_blueprint

    app.register_blueprint(tarefa_blueprint)
    app.register_blueprint(projeto_blueprint)
    app.register_blueprint(funcionario_blueprint)
    app.register_blueprint(usuario_blueprint)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return (
                decrypted_token["jti"] in BLACKLIST
        )

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db, "ma": ma, "migrate": migrate}

    return app
