# Generated by Django 3.1.6 on 2021-04-07 02:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210405_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 22, 22, 22, 993046)),
        ),
    ]
