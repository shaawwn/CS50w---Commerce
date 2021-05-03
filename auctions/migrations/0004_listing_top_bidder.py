# Generated by Django 3.2 on 2021-05-03 00:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='top_bidder',
            field=models.ManyToManyField(blank=True, default=None, related_name='top_bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
