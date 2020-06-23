from flask import Blueprint, request
from flask_restful import Resource, Api
from marshmallow import ValidationError

from sistema.api.helpers.paginacao import paginacao
from sistema.api.models.projeto import ProjetoModel
from sistema.api.schemas.projeto import ProjetoSchema

projeto_blueprint = Blueprint("projeto", __name__)
api = Api(projeto_blueprint)

ERRO_INSERT = "Ocorreu um erro ao inserir o projeto."
PROJETO_NOT_FOUND = "Projeto não encontrado."
PROJETO_EXCLUIDO = "Projeto excluída com sucesso."

projeto_schema = ProjetoSchema()
projeto_list_schema = ProjetoSchema(many=True)


class Projeto(Resource):
    @classmethod
    def post(cls):
        projeto_json = request.get_json()
        try:
            projeto = projeto_schema.load(projeto_json)
        except ValidationError as err:
            print(err)
            return err.messages, 400

        try:
            projeto.save_to_db()
        except Exception as e:
            return {"mensagem": ERRO_INSERT}, 500

        return projeto_schema.dump(projeto), 201


class ProjetoDetalhes(Resource):
    @classmethod
    def get(cls, projeto_id: int):
        projeto = ProjetoModel.find_by_id(projeto_id)
        if not projeto:
            return {"mensagem": PROJETO_NOT_FOUND}, 404
        return projeto_schema.dump(projeto), 200

    @classmethod
    def put(cls, projeto_id: int):
        projeto_json = request.get_json()
        projeto = ProjetoModel.find_by_id(projeto_id)
        if not projeto:
            return {"mensagem": PROJETO_NOT_FOUND}, 404

        if projeto:
            try:
                validate = projeto_schema.validate(projeto_json)
                if validate:
                    return validate, 400
                else:
                    projeto.titulo = projeto_json["nome"]
                    projeto.descricao = projeto_json["descricao"]
            except ValidationError as err:
                return err.messages, 400
        try:
            projeto.save_to_db()
        except Exception as e:
            print(e)
        return projeto_schema.dump(projeto), 200

    @classmethod
    def delete(cls, projeto_id: int):
        projeto = ProjetoModel.find_by_id(projeto_id)
        if not projeto:
            return {"mensagem": PROJETO_NOT_FOUND}, 404
        projeto.delete_from_db()
        return {"mensagem": PROJETO_EXCLUIDO}, 200


class ProjetoList(Resource):
    @classmethod
    def get(cls):
        return paginacao(ProjetoModel, projeto_list_schema), 200


api.add_resource(Projeto, "/projeto")
api.add_resource(ProjetoDetalhes, "/projeto/<int:projeto_id>")
api.add_resource(ProjetoList, "/projetos")
