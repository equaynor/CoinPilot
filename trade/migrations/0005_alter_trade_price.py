# Generated by Django 4.2.11 on 2024-05-23 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_remove_trade_timestamp_trade_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='price',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=18),
        ),
    ]
