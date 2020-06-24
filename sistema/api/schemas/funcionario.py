from sistema import ma
from sistema.api.models.funcionario import FuncionarioModel


class FuncionarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FuncionarioModel
        include_fk = True
        load_instance = True

    _links = ma.Hyperlinks(
        {
            "get": ma.URLFor("funcionario.funcionariodetalhes", funcionario_id="<id>"),
            "put": ma.URLFor("funcionario.funcionariodetalhes", funcionario_id="<id>"),
            "del": ma.URLFor("funcionario.funcionariodetalhes", funcionario_id="<id>"),
        }
    )
