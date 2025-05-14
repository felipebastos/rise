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
    ("dbr", "Debuff de rage"),
    ("car", "Dano de contra-ataque recebido"),
    ("cac", "Dano de contra-ataque causado"),
    ("dbr", "Debuff de rage"),
    ("dbd", "Debuff de defesa"),
    ("dbs", "Debuff de saúde"),
    ("dvc", "Debuff de velocidade de cavalaria"),
    ("esc", "Escudo"),
    ("hab", "Dano de habilidade"),
    ("ano", "Dano de ataque normal"),
    ("bra", "Bônus de rage"),
    ("bad", "Aumento de dano"),
    ("baa", "Aumento de ataque em área"),
    ("dbd", "Debuff de defesa"),
)

POSICAO = (
    ("cap", "Capacete"),
    ("pei", "Peitoral"),
    ("luv", "Luva"),
    ("arm", "Armamento"),
    ("cal", "Calça"),
    ("bot", "Bota"),
    ("ace", "Acessório"),
)


def picture_directory_path(instance, filename):
    """Trouxe direto da documentação, para simplificar."""
    # file will be uploaded to MEDIA_ROOT/equip_<id>/<filename>
    extension = filename.split(".")[-1]
    return f"equip_{instance.id}/equipment_pic.{extension}"


class Equipamento(models.Model):
    nome = models.CharField(max_length=45, unique=True)
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
    spec = models.CharField("Especialidade", max_length=3, choices=SPECS, default="tod")
    status = models.CharField(max_length=3, choices=STATUS, default="atq")
    valor = models.FloatField()
    ativacao = models.FloatField("Ativação", default=1.0)


kits = (
    ("2", "2"),
    ("4", "4"),
    ("6", "6"),
)


class BuffConjunto(models.Model):
    conjunto = models.ForeignKey(
        "Conjunto", related_name="buff_conjunto", on_delete=models.CASCADE
    )
    spec = models.CharField("Especialidade", max_length=3, choices=SPECS, default="tod")
    status = models.CharField(max_length=3, choices=STATUS, default="atq")
    valor = models.FloatField()
    ativacao = models.FloatField("Ativação", default=1.0)
    pecas = models.CharField("Peças", max_length=1, choices=kits, default="2")


class Conjunto(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    conjunto = models.ManyToManyField(Equipamento)

    def get_buffs(self, conjunto):
        quantidade = 0

        for peca in self.conjunto.all():
            if peca in conjunto:
                quantidade = quantidade + 1

        buffs = BuffConjunto.objects.filter(conjunto=self, pecas__lte=quantidade)

        return buffs
