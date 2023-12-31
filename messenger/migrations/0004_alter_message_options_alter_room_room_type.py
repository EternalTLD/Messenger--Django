# Generated by Django 4.2.4 on 2023-09-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messenger", "0003_room_admin_alter_room_participants"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.AlterField(
            model_name="room",
            name="room_type",
            field=models.CharField(
                choices=[("D", "Direct"), ("G", "Group")], max_length=1
            ),
        ),
    ]
