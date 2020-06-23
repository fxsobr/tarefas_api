from flask import Blueprint, request
from flask_restful import Resource, Api
from marshmallow import ValidationError

from sistema.api.models.tarefa import TarefaModel
from sistema.api.schemas import tarefa
from sistema.api.schemas.tarefa import TarefaSchema

tarefa_blueprint = Blueprint("tarefa", __name__)
api = Api(tarefa_blueprint)

ERRO_INSERT = "Ocorreu um erro ao inserir a tarefa."
TAREFA_NOT_FOUND = "Tarefa não encontrada."
TAREFA_EXCLUIDA = "Tarefa excluída com sucesso."

tarefa_schema = TarefaSchema()
tarefa_list_schema = TarefaSchema(many=True)


class Tarefa(Resource):
    @classmethod
    def post(cls):
        tarefa_json = request.get_json()
        try:
            tarefa = tarefa_schema.load(tarefa_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            tarefa.save_to_db()
        except Exception as e:
            return {"mensagem": ERRO_INSERT}, 500

        return tarefa_schema.dump(tarefa), 201


class TarefaDetalhes(Resource):
    @classmethod
    def get(cls, tarefa_id: int):
        tarefa = TarefaModel.find_by_id(tarefa_id)
        if not tarefa:
            return {"mensagem": TAREFA_NOT_FOUND}, 404
        return tarefa_schema.dump(tarefa), 200

    @classmethod
    def put(cls, tarefa_id: int):
        tarefa_json = request.get_json()
        tarefa = TarefaModel.find_by_id(tarefa_id)
        if not tarefa:
            return {"mensagem": TAREFA_NOT_FOUND}, 404

        if tarefa:
            try:
                validate = tarefa_schema.validate(tarefa_json)
                if validate:
                    return validate, 400
                else:
                    tarefa.titulo = tarefa_json["titulo"]
                    tarefa.descricao = tarefa_json["descricao"]
                    tarefa.data_expiracao = tarefa_json["data_expiracao"]
            except ValidationError as err:
                return err.messages, 400
        try:
            tarefa.save_to_db()
        except Exception as e:
            print(e)
        return tarefa_schema.dump(tarefa), 200

    @classmethod
    def delete(cls, tarefa_id: int):
        tarefa = TarefaModel.find_by_id(tarefa_id)
        if not tarefa:
            return {"mensagem": TAREFA_NOT_FOUND}, 404
        tarefa.delete_from_db()
        return {"mensagem": TAREFA_EXCLUIDA}, 200


class TarefaList(Resource):
    @classmethod
    def get(cls):
        return {"tarefas": tarefa_list_schema.dump(TarefaModel.find_all())}, 200


api.add_resource(Tarefa, "/tarefa")
api.add_resource(TarefaDetalhes, "/tarefa/<int:tarefa_id>")
api.add_resource(TarefaList, "/tarefas")
