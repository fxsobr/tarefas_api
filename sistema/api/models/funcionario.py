from typing import List

from sistema import db


class FuncionarioModel(db.Model):
    __tablename__ = "funcionario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefone_celular = db.Column(db.String(12), nullable=False)
    endereco_rua = db.Column(db.String(512), nullable=False)
    endereco_bairro = db.Column(db.String(50), nullable=False)
    endereco_numero = db.Column(db.Integer, nullable=False)
    endereco_cidade = db.Column(db.String(25), nullable=False)
    endereco_estado = db.Column(db.String(50), nullable=False)
    endereco_complemento = db.Column(db.String(50), nullable=False)
    endereco_cep = db.Column(db.Integer, nullable=False)

    tarefa_id = db.Column(db.Integer, db.ForeignKey("tarefa.id"))
    tarefa = db.relationship(
        "TarefaModel", backref=db.backref("funcionarios", lazy="dynamic")
    )

    @classmethod
    def find_all(cls) -> List["FuncionarioModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "FuncionarioModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
