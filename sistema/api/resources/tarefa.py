from flask import Blueprint, request
from flask_restful import Resource, Api
from marshmallow import ValidationError

from sistema.api.models.tarefamodel import TarefaModel
from sistema.api.schemas import tarefa
from sistema.api.schemas.tarefa import TarefaSchema

tarefa_blueprint = Blueprint("tarefa", __name__)
api = Api(tarefa_blueprint)

ERRO_INSERT = "Ocorreu um erro ao inserir a tarefa!"

tarefa_schema = TarefaSchema()
tarefa_list_schema = TarefaSchema(many=True)


class Tarefa(Resource):
    @classmethod
    def post(cls):
        tarefa_json = request.get_json()
        try:
            tarefa = tarefa_schema.load(tarefa_json)
            print(tarefa)
        except ValidationError as err:
            return err.messages, 400

        try:
            tarefa.save_to_db()
        except Exception as e:
            return {"mensagem": ERRO_INSERT}, 500

        return tarefa_schema.dump(tarefa), 201


class TarefaList(Resource):
    @classmethod
    def get(cls):
        return {"tarefas": tarefa_list_schema.dump(TarefaModel.find_all())}, 200


api.add_resource(Tarefa, "/tarefa")
api.add_resource(TarefaList, "/tarefas")
