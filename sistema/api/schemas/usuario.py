from sistema import ma
from sistema.api.models.usuario import UsuarioModel


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_only = ("senha",)
        dump_only = ("id",)
        load_instance = True