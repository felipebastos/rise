# Generated by Django 4.1.2 on 2022-10-17 15:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mge", "0014_mge_livre_mge_temporada"),
    ]

    operations = [
        migrations.AddField(
            model_name="mge",
            name="inicio_das_inscricoes",
            field=models.DateField(null=True, verbose_name="Início das inscrições"),
        ),
    ]
