# Generated by Django 5.0.3 on 2024-04-11 08:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminBond',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isin', models.CharField(max_length=255, unique=True)),
                ('space', models.CharField(choices=[('UEMOA', 'Union économique et monétaire ouest-africaine (UEMOA) '), ('CEMAC', "Communauté économique et monétaire de l'Afrique centrale (CEMAC)"), ('COMORES', 'Union des Comores (UC)'), ('UEAC', "Union des États de l'Afrique centrale (UEAC)"), ('UA', 'Union africaine (UA)')], default='UEMOA', max_length=255)),
                ('description', models.TextField()),
                ('entity', models.CharField(choices=[('Country', 'Country'), ('Society', 'Society')], default=0, max_length=20)),
                ('due_date', models.DateField()),
                ('facial_rate', models.FloatField()),
                ('refund', models.CharField(choices=[('IF', 'In Fine'), ('AC', 'Constant Amortissable'), ('ACD', 'Differed Constant Amortissable')], default='IF', max_length=5)),
                ('differed', models.IntegerField()),
                ('guarantee', models.CharField(max_length=100)),
                ('total_number', models.IntegerField()),
                ('type', models.CharField(max_length=50)),
                ('period', models.CharField(choices=[('T', 'Trimestrial'), ('S', 'Semestrial'), ('A', 'Annual')], default='A', max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
