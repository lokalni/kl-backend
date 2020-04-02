# Generated by Django 2.2.10 on 2020-04-02 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kl_backend.utils
import kl_participants.models.moderator


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kl_participants', '0003_auto_20200401_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderator',
            name='access_token',
            field=models.CharField(default=kl_backend.utils.get_token, max_length=8, unique=True),
        ),
        migrations.AddField(
            model_name='moderator',
            name='user',
            field=models.OneToOneField(default=kl_participants.models.moderator.empty_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='access_token',
            field=models.CharField(default=kl_backend.utils.get_token, max_length=8, unique=True),
        ),
    ]
