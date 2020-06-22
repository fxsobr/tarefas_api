from sistema import ma
from sistema.api.models import tarefamodel
from marshmallow import fields


class TarefaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = tarefamodel.TarefaModel
        fields = ("id", "titulo", "descricao", "data_expiracao")

    titulo = fields.String(required=True)
    descricao = fields.String(required=True)
    data_expiracao = fields.Date(required=True)