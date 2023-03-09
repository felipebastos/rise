from typing import Type

from django import forms


class RiseTaskResponse:
    def __init__(self, mensagem: str, status: int = 200) -> None:
        self.status = status
        self.mensagem = mensagem

    def __str__(self) -> str:
        return f'Task Status <{self.status}>: "{self.mensagem}"'

    def __repr__(self) -> str:
        return f"<RiseTaskResponse {self.status}>"


class RiseTask:
    def __init__(
        self, nome: str = "Não definido", descricao: str = "Sem descrição"
    ) -> None:
        self.nome = nome
        self.descricao = descricao

    def run(self, from_form: forms.Form = None) -> RiseTaskResponse:
        pass

    def form_class(self) -> Type[forms.Form]:
        pass
