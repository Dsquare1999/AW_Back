# Generated by Django 5.0.3 on 2024-04-12 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alm', '0005_alter_bond_cashflows_alter_bond_duration_macaulay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='annual_coupon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
