# Generated by Django 4.2.11 on 2024-05-06 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_portfolio_user'),
        ('holding', '0001_initial'),
        ('coin', '0001_initial'),
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='coin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coin.coin'),
        ),
        migrations.AddField(
            model_name='trade',
            name='portfolio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='portfolio.portfolio'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='holding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='holding.holding'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='trade',
            name='quantity',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='trade',
            name='trade_type',
            field=models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], default='BUY', max_length=4),
        ),
    ]
