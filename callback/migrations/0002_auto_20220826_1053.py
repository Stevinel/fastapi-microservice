# Generated by Django 3.2.5 on 2022-08-26 10:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callback', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name': 'Game', 'verbose_name_plural': 'Games'},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'Player', 'verbose_name_plural': 'Players'},
        ),
        migrations.AddField(
            model_name='game',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 8, 26, 10, 53, 15, 561716)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='player',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 8, 26, 10, 53, 17, 894451)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(default='', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(max_length=54, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default='', max_length=54, unique=True),
        ),
    ]
