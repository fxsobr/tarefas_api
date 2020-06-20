from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('sistema.config.DevelopmentConfig')

api = Api(app)

from .resources import tarefa