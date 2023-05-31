# Generated by Django 4.2 on 2023-05-31 15:09

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_language_iso_639_1_alter_language_iso_639_2_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
