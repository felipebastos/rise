import os

from django import forms
from django.conf import settings

from tasks.scripts.script import RiseTask, RiseTaskResponse


class SoftwareStatsTask(RiseTask):
    def run(self, from_form: forms.Form = None) -> RiseTaskResponse:
        lines_of_code = 0
        source_files = 0

        root = os.listdir(settings.BASE_DIR)
        for item in root:
            if os.path.isdir(item) and item not in [
                ".venv",
                ".vscode",
                ".git",
                "static",
                "media",
                ".github",
            ]:
                os.chdir(os.path.join(settings.BASE_DIR, item))
                inner = os.listdir()

                for inside in inner:
                    os.chdir(os.path.join(settings.BASE_DIR, item))
                    if os.path.isfile(inside) and (
                        inside.endswith(".py") or inside.endswith(".html")
                    ):
                        source_files = source_files + 1
                        with open(
                            os.path.join(settings.BASE_DIR, item, inside),
                            "r",
                            encoding="UTF-8",
                        ) as source:
                            contagem = 0
                            for count, _ in enumerate(source):
                                contagem = count
                            lines_of_code = lines_of_code + contagem + 1
                    elif os.path.isdir(inside) and inside == "templates":
                        os.chdir(os.path.join(settings.BASE_DIR, item, inside, item))
                        in_inside = os.listdir()
                        for template in in_inside:
                            if os.path.isfile(template) and (
                                template.endswith(".html")
                            ):
                                source_files = source_files + 1
                                with open(
                                    os.path.join(
                                        settings.BASE_DIR,
                                        item,
                                        inside,
                                        item,
                                        template,
                                    ),
                                    "r",
                                    encoding="UTF-8",
                                ) as source:
                                    contagem = 0
                                    for count, _ in enumerate(source):
                                        contagem = count
                                    lines_of_code = lines_of_code + contagem + 1

                    elif os.path.isdir(inside) and inside == "migrations":
                        os.chdir(os.path.join(settings.BASE_DIR, item, inside))
                        in_inside = os.listdir()
                        for migration in in_inside:
                            if os.path.isfile(migration) and (
                                migration.endswith(".py")
                            ):
                                source_files = source_files + 1
                                with open(
                                    os.path.join(
                                        settings.BASE_DIR,
                                        item,
                                        inside,
                                        migration,
                                    ),
                                    "r",
                                    encoding="UTF-8",
                                ) as source:
                                    contagem = 0
                                    for count, _ in enumerate(source):
                                        contagem = count
                                    lines_of_code = lines_of_code + contagem + 1

                os.chdir(settings.BASE_DIR)
            elif item.endswith(".py") or item.endswith(".html"):
                source_files = source_files + 1

                with open(
                    os.path.join(settings.BASE_DIR, item),
                    "r",
                    encoding="UTF-8",
                ) as source:
                    contagem = 0
                    for count, _ in enumerate(source):
                        contagem = count
                    lines_of_code = lines_of_code + contagem + 1
        mensagem = f"O projeto tem {source_files} arquivos de código \
                                 e um total de {lines_of_code} linhas de código."

        response = RiseTaskResponse(mensagem)
        return response

    def render(self) -> forms.BaseForm:
        return None


def main() -> RiseTask:
    return SoftwareStatsTask(
        nome="Levanta dados do código fonte",
        descricao="Varre o repositório e verifica o tamanho do projeto \
                            do ponto de vista de linhas de código html e python.",
    )
