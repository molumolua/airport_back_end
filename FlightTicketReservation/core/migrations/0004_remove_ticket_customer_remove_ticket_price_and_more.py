# Generated by Django 4.1.7 on 2023-05-26 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_passenger"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="ticket",
            name="price",
        ),
        migrations.AddField(
            model_name="ticket",
            name="passenger",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.passenger",
            ),
        ),
        migrations.CreateModel(
            name="Order",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.flight"
                    ),
                ),
                ("tickets", models.ManyToManyField(to="core.ticket")),
            ],
        ),
    ]
