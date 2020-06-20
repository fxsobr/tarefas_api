from flask_restful import Resource
from sistema import api


class TarefaList(Resource):
    def get(self):
        return "Olá Mundo", 200


api.add_resource(TarefaList, '/tarefas')
