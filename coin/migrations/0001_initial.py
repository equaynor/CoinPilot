# Generated by Django 4.2.11 on 2024-04-29 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_id', models.CharField(default='', max_length=255, unique=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('symbol', models.CharField(default='', max_length=50)),
                ('current_price', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('image', models.URLField(default='')),
                ('market_cap', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('market_cap_rank', models.IntegerField(default=0)),
                ('price_change_percentage_24h', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('ath', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('ath_date', models.DateTimeField(null=True)),
                ('circulating_supply', models.DecimalField(decimal_places=2, max_digits=30, null=True)),
                ('total_supply', models.DecimalField(decimal_places=2, max_digits=30, null=True)),
                ('max_supply', models.DecimalField(decimal_places=2, max_digits=30, null=True)),
                ('categories', models.JSONField(default=list)),
            ],
        ),
    ]
