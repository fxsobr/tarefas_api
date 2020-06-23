from flask import Blueprint, request
from flask_restful import Resource, Api
from marshmallow import ValidationError

from sistema.api.models.funcionario import FuncionarioModel
from sistema.api.schemas.funcionario import FuncionarioSchema

funcionario_blueprint = Blueprint("funcionario", __name__)
api = Api(funcionario_blueprint)

ERRO_INSERT = "Ocorreu um erro ao inserir o funcionário."
FUNCIONARIO_NOT_FOUND = "Funcionário não encontrado."
FUNCIONARIO_EXCLUIDO = "Funcionário excluída com sucesso."

funcionario_schema = FuncionarioSchema()
funcionario_list_schema = FuncionarioSchema(many=True)


class Funcionario(Resource):
    @classmethod
    def post(cls):
        funcionario_json = request.get_json()
        try:
            funcionario = funcionario_schema.load(funcionario_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            funcionario.save_to_db()
        except Exception as e:
            return {"mensagem": ERRO_INSERT}, 500

        return funcionario_schema.dump(funcionario), 201


class FuncionarioDetalhes(Resource):
    @classmethod
    def get(cls, funcionario_id: int):
        funcionario = FuncionarioModel.find_by_id(funcionario_id)
        if not funcionario:
            return {"mensagem": FUNCIONARIO_NOT_FOUND}, 404
        return funcionario_schema.dump(funcionario), 200

    @classmethod
    def put(cls, funcionario_id: int):
        funcionario_json = request.get_json()
        funcionario = FuncionarioModel.find_by_id(funcionario_id)
        if not funcionario:
            return {"mensagem": FUNCIONARIO_NOT_FOUND}, 404

        if funcionario:
            try:
                validate = funcionario_schema.validate(funcionario_json)
                if validate:
                    return validate, 400
                else:
                    funcionario.titulo = funcionario_json["nome"]
                    funcionario.descricao = funcionario_json["descricao"]
            except ValidationError as err:
                return err.messages, 400
        try:
            funcionario.save_to_db()
        except Exception as e:
            print(e)
        return funcionario_schema.dump(funcionario), 200

    @classmethod
    def delete(cls, funcionario_id: int):
        funcionario = FuncionarioModel.find_by_id(funcionario_id)
        if not funcionario:
            return {"mensagem": FUNCIONARIO_NOT_FOUND}, 404
        funcionario.delete_from_db()
        return {"mensagem": FUNCIONARIO_EXCLUIDO}, 200


class FuncioarioList(Resource):
    @classmethod
    def get(cls):
        return {"funcionários": funcionario_list_schema.dump(FuncionarioModel.find_all())}, 200


api.add_resource(Funcionario, "/projeto")
api.add_resource(FuncionarioDetalhes, "/projeto/<int:projeto_id>")
api.add_resource(FuncioarioList, "/projetos")
