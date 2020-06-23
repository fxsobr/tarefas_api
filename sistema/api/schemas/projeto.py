from sistema import ma

from sistema.api.models.projeto import ProjetoModel


class ProjetoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjetoModel
        load_instance = True
