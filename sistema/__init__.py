import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from sistema.api.resources.tarefa import tarefa_blueprint
    from sistema.api.resources.projeto import projeto_blueprint
    from sistema.api.resources.funcionario import funcionario_blueprint

    app.register_blueprint(tarefa_blueprint)
    app.register_blueprint(projeto_blueprint)
    app.register_blueprint(funcionario_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db, "ma": ma, "migrate": migrate}

    return app
