from django.db import models

# Create your models here.
SPECS = (
    ("arq", "Arquearia"),
    ("cav", "Cavalaria"),
    ("inf", "Infantaria"),
    ("tod", "Geral"),
)

STATUS = (
    ("atq", "Ataque"),
    ("def", "Defesa"),
    ("sau", "Saúde"),
    ("vel", "Velocidade"),
)

POSICAO = (
    ("cap", "Capacete"),
    ("pei", "Peitoral"),
    ("luv", "Luva"),
    ("arm", "Armamento"),
    ("cal", "Calça"),
    ("bot", "Bota"),
    ("ace", "Acessório esquerdo"),
    ("acd", "Acessório direito"),
)


def picture_directory_path(instance, filename):
    """Trouxe direto da documentação, para simplificar."""
    # file will be uploaded to MEDIA_ROOT/equip_<id>/<filename>
    extension = filename.split(".")[-1]
    return f"equip_{instance.id}/equipment_pic.{extension}"


class Equipamento(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    miniatura = models.ImageField(
        blank=True,
        upload_to=picture_directory_path,
        default="defaults/equipment.png",
    )
    slot = models.CharField(max_length=3, choices=POSICAO, default="cap")

    def __str__(self) -> str:
        return f"{self.nome}"


class Buff(models.Model):
    equipamento = models.ForeignKey(
        Equipamento, related_name="buffs", on_delete=models.CASCADE
    )
    spec = models.CharField(
        "Especialidade", max_length=3, choices=SPECS, default="tod"
    )
    status = models.CharField(max_length=3, choices=STATUS, default="atq")
    valor = models.FloatField()
    ativacao = models.FloatField("Ativação", default=1.0)
