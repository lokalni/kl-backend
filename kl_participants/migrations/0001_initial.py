# Generated by Django 2.2.10 on 2020-03-25 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=255)),
                ('region', models.CharField(choices=[('dolnoslaskie', 'dolnoslaskie'), ('slaskie', 'slaskie')], max_length=32)),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=255)),
                ('access_token', models.CharField(max_length=8)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kl_participants.Group')),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(to='kl_participants.Group')),
            ],
            options={
                'db_table': 'moderators',
            },
        ),
    ]
