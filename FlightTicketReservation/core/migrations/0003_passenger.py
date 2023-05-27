# Generated by Django 4.1.7 on 2023-05-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_seat_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="Passenger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_card_number", models.CharField(max_length=18, unique=True)),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
            ],
        ),
    ]
