# Generated by Django 5.0.3 on 2024-04-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alm', '0002_rename_reference_course_bond_reference_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='guarantee',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bond',
            name='reference_value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='bond',
            name='refinancing',
            field=models.CharField(max_length=100),
        ),
    ]
