from sistema import ma

from sistema.api.models.projeto import ProjetoModel
from sistema.api.models.tarefa import TarefaModel
from sistema.api.schemas.tarefa import TarefaSchema


class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    tarefas = ma.Nested(TarefaSchema, many=True)
    class Meta:
        model = ProjetoModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True

    _links = ma.Hyperlinks(
        {
            "get": ma.URLFor("projeto.projetodetalhes", projeto_id="<id>"),
            "put": ma.URLFor("projeto.projetodetalhes", projeto_id="<id>"),
            "del": ma.URLFor("projeto.projetodetalhes", projeto_id="<id>"),
        }
    )

