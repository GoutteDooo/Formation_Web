# Generated by Django 5.2.1 on 2025-05-31 10:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
