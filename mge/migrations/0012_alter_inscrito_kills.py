# Generated by Django 4.0.6 on 2022-08-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mge", "0011_inscrito_intuito"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inscrito",
            name="kills",
            field=models.BigIntegerField(default=0),
        ),
    ]
