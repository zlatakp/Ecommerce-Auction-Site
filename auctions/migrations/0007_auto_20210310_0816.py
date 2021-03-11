# Generated by Django 3.1.6 on 2021-03-10 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210310_0814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='start_bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='start_bid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
