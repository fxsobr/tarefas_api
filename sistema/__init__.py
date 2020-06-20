import os

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

api = Api(app)

from .resources import tarefa