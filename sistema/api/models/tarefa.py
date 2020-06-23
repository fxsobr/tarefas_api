from typing import List

from sistema import db
from sistema.api.models.projeto import ProjetoModel


class TarefaModel(db.Model):
    __tablename__ = "tarefa"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    titulo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    data_expiracao = db.Column(db.Date, nullable=False)

    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"))
    projeto = db.relationship("ProjetoModel", backref=db.backref("tarefas", lazy="dynamic"))

    @classmethod
    def find_all(cls) -> List["TarefaModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "TarefaModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
