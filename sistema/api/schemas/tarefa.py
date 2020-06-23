from sistema import ma

from sistema.api.models.tarefa import TarefaModel
from sistema.api.schemas.funcionario import FuncionarioSchema


class TarefaSchema(ma.SQLAlchemyAutoSchema):
    funcionarios = ma.Nested(FuncionarioSchema, many=True)
    class Meta:
        model = TarefaModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True

