# Generated by Django 5.1.1 on 2024-09-24 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kvk", "0021_batalha"),
    ]

    operations = [
        migrations.AddField(
            model_name="consolidado",
            name="t4_kill",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="consolidado",
            name="t5_kill",
            field=models.IntegerField(default=0),
        ),
    ]
