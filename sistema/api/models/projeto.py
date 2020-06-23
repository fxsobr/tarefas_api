from typing import List

from sistema import db
from sistema.api.models.funcionario import FuncionarioModel


class ProjetoModel(db.Model):
    __tablename__ = "projeto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)

    @classmethod
    def find_all(cls) -> List["ProjetoModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "ProjetoModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
