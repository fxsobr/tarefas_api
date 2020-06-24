from flask import request, Blueprint
from flask_restful import Resource, Api
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from marshmallow import ValidationError

from sistema.api.helpers.blacklist import BLACKLIST
from sistema.api.models.usuario import UsuarioModel
from sistema.api.schemas.usuario import UsuarioSchema

usuario_blueprint = Blueprint("usuario", __name__)
api = Api(usuario_blueprint)

NAME_ALREADY_EXISTS = "Um usuário com esse nome já existe!"
USER_CREATED = "Usuario criado com sucesso!"
USER_NOT_FOUND = "Usuario não encontrado."
USER_LOGOUT = "Usuario <id={}> deslogado com sucesso!"
USER_INVALID_CREDENTIALS = "Credenciais Inválidas!"

usuario_schema = UsuarioSchema()


class UsuarioRegistro(Resource):
    @classmethod
    def post(cls):
        try:
            usuario = usuario_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if UsuarioModel.find_by_usuario(usuario.usuario):
            return {"mensagem": NAME_ALREADY_EXISTS}, 400

        usuario.save_to_db()

        return {"mensagem": USER_CREATED}, 201


class UsuarioLogin(Resource):
    @classmethod
    def post(cls):
        try:
            usuario_json = request.get_json()
            usuario_data = usuario_schema.load(usuario_json)
        except ValidationError as err:
            return err.messages, 400

        usuario = UsuarioModel.find_by_usuario(usuario_data.usuario)

        if usuario and safe_str_cmp(usuario.senha, usuario_data.senha):
            access_token = create_access_token(identity=usuario.id, fresh=True)
            refresh_token = create_refresh_token(usuario.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"mensagem": USER_INVALID_CREDENTIALS}, 401


class UsuarioLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"mensagem": USER_LOGOUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


api.add_resource(UsuarioRegistro, "/registrar")
api.add_resource(UsuarioLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UsuarioLogout, "/logout")
