# Generated by Django 4.2.11 on 2024-05-24 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('holding', '0002_holding_quantity'),
        ('trade', '0005_alter_trade_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='holding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_trades', to='holding.holding'),
        ),
    ]
