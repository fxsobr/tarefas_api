from sistema import ma

from sistema.api.models.tarefa import TarefaModel
from sistema.api.models.projeto import ProjetoModel


class TarefaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TarefaModel
        include_fk = True
        load_instance = True
