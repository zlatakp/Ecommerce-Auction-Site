# Generated by Django 3.1.6 on 2021-03-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210310_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='WatchedBy', to='auctions.Listing'),
        ),
    ]
