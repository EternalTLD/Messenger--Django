# Generated by Django 4.2.4 on 2023-08-18 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendshipRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('rejected_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата отклонения')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_sent', to=settings.AUTH_USER_MODEL, verbose_name='От пользователя')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_recived', to=settings.AUTH_USER_MODEL, verbose_name='К пользователю')),
            ],
            options={
                'verbose_name': 'Заявка в друзья',
                'verbose_name_plural': 'Заявки в друзья',
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL, verbose_name='От пользователя')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_friends', to=settings.AUTH_USER_MODEL, verbose_name='К пользователю')),
            ],
            options={
                'verbose_name': 'Друг',
                'verbose_name_plural': 'Друзья',
                'unique_together': {('from_user', 'to_user')},
            },
        ),
    ]
