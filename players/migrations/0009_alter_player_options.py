# Generated by Django 3.2.3 on 2021-07-01 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0008_auto_20210701_1635"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="player",
            options={"ordering": ["nick"]},
        ),
    ]
