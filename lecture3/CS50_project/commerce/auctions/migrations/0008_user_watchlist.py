# Generated by Django 5.2.1 on 2025-05-31 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_picture_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlisted_by', to='auctions.listing'),
        ),
    ]
