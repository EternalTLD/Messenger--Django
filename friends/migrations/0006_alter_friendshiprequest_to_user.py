# Generated by Django 4.2.4 on 2023-11-19 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "friends",
            "0005_alter_friend_options_alter_friendshiprequest_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="friendshiprequest",
            name="to_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friendship_requests_received",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
