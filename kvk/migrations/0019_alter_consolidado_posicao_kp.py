# Generated by Django 4.2 on 2023-07-11 01:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kvk", "0018_rename_cor_consolidado_cor_dt_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consolidado",
            name="posicao_kp",
            field=models.IntegerField(null=True),
        ),
    ]
