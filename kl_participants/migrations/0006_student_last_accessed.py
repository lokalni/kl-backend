# Generated by Django 2.2.10 on 2020-04-25 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kl_participants', '0005_auto_20200406_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='last_accessed',
            field=models.DateTimeField(null=True),
        ),
    ]
