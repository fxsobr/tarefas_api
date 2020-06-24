from sistema import db


class UsuarioModel(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable=False, unique=True)
    senha = db.Column(db.String(80), nullable=False)

    @classmethod
    def find_by_usuario(cls, usuario: str) -> "UsuarioModel":
        return cls.query.filter_by(usuario=usuario).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UsuarioModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
