# Generated by Django 3.1.6 on 2021-03-22 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_listing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='winner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='wonitems', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biddeditems', to=settings.AUTH_USER_MODEL),
        ),
    ]