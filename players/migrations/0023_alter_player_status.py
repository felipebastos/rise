# Generated by Django 4.1 on 2022-08-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0022_alter_advertencia_inicio_alter_playerstatus_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="status",
            field=models.CharField(
                choices=[
                    ("PLAYER", "Player"),
                    ("SECUNDARIA", "Secundária"),
                    ("FARM", "Farm"),
                    ("INATIVO", "Inativo"),
                    ("MIGROU", "Migrou"),
                    ("VIGIAR", "Vigiar"),
                    ("BANIDO", "BANIDO"),
                ],
                default="PLAYER",
                max_length=100,
            ),
        ),
    ]
