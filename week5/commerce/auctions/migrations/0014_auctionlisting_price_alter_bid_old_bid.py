# Generated by Django 4.1.3 on 2023-01-15 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auctionlisting_isactive_auctionlisting_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='old_bid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
