import os

from django import forms
from django.conf import settings
from PIL import Image

from tasks.scripts.script import RiseTask, RiseTaskResponse


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


class ResizeTask(RiseTask):
    def run(self, from_form: forms.Form = None) -> RiseTaskResponse:
        quantidade = 0

        estava_ocupando = 0
        economia = 0

        os.chdir(settings.MEDIA_ROOT)

        pastas = os.listdir(settings.MEDIA_ROOT)

        for pasta in pastas:
            os.chdir(os.path.join(settings.MEDIA_ROOT, pasta))
            arquivos = os.listdir()
            for imagem in arquivos:
                print(f"Trabalhando em {os.getcwd()}")
                img = Image.open(imagem)
                print("[*] Image shape:", img.size)
                shape_x, shape_y = img.size

                image_size = os.path.getsize(imagem)
                if shape_x > 64 or shape_y > 64:
                    print(
                        "[*] Size before compression:",
                        get_size_format(image_size),
                    )
                    img = img.resize((64, 64), Image.ANTIALIAS)
                    print("[+] New Image shape:", img.size)
                    try:
                        img.save(imagem, quality=75, optimize=True)
                    except OSError:
                        img = img.convert("RGB")
                        img.save(imagem, quality=75, optimize=True)
                    print("[+] New file saved:", imagem)
                    new_image_size = os.path.getsize(imagem)
                    estava_ocupando = estava_ocupando + image_size
                    economia = economia + new_image_size
                    quantidade = quantidade + 1
                    print(
                        "[+] Size after compression:",
                        get_size_format(new_image_size),
                    )
                    saving_diff = new_image_size - image_size
                    print(
                        f"[+] Image size change: {saving_diff/image_size*100:.2f}% \
                          of the original image size."
                    )
                else:
                    print(f"Mantendo o tamanho original de {imagem}")

        mensagem = "Não foi necessário realizar alterações."
        if estava_ocupando > 0:
            mensagem = f"{quantidade} imagens otimizadas. Economia de {economia/estava_ocupando*100:.2f}% do espaço de armazenamento usado antes."

        response = RiseTaskResponse(mensagem)
        return response

    def render(self) -> forms.BaseForm:
        return None


def main() -> RiseTask:
    return ResizeTask(
        nome="Otimiza o tamanho das imagens armazenadas",
        descricao="Reduz o tamanho e a qualidade das imagens armazenadas \
                            para liberar espaço.",
    )
