# Generated by Django 4.1.3 on 2023-01-16 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auctionlisting_price_alter_bid_old_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='isActive',
        ),
        migrations.AddField(
            model_name='listing',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]