# Generated by Django 3.1.6 on 2021-03-16 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_bid_start_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='final_bid',
        ),
    ]