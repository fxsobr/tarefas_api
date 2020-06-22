import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

from .resources import tarefa