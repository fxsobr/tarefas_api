from sistema import ma
from sistema.api.models.funcionario import FuncionarioModel


class FuncionarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FuncionarioModel
        load_instance = True
