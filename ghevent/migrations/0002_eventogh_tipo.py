# Generated by Django 4.2.10 on 2024-03-02 19:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ghevent", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventogh",
            name="tipo",
            field=models.CharField(
                choices=[("pow", "poder"), ("acc", "aceleração")],
                default="pow",
                max_length=3,
            ),
        ),
    ]
