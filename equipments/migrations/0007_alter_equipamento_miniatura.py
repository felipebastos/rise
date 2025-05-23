# Generated by Django 4.1.2 on 2022-10-26 02:27

from django.db import migrations, models

import equipments.models


class Migration(migrations.Migration):
    dependencies = [
        ("equipments", "0006_equipamento_slot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipamento",
            name="miniatura",
            field=models.ImageField(
                blank=True,
                default="defaults/equipment.png",
                upload_to=equipments.models.picture_directory_path,
            ),
        ),
    ]
