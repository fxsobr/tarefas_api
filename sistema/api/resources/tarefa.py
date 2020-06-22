from flask import Blueprint
from flask_restful import Resource
from flask_restful import Resource, Api

tarefa_blueprint = Blueprint('tarefa', __name__)
api = Api(tarefa_blueprint)


class TarefaList(Resource):
    def get(self):
        return "Olá Mundo", 200


api.add_resource(TarefaList, '/tarefas')
