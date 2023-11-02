# Generated by Django 4.2.4 on 2023-09-05 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("friends", "0003_block"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="to_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="in_black_list",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Заблокированный",
            ),
        ),
    ]