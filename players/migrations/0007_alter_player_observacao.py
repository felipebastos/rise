# Generated by Django 3.2.3 on 2021-07-01 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0006_alter_player_observacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="observacao",
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]
