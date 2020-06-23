from sistema import ma

from sistema.api.models.tarefa import TarefaModel


class TarefaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TarefaModel
        load_instance = True
