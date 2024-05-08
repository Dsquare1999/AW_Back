# Generated by Django 5.0.3 on 2024-05-07 09:55

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bilan', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PIBPortofolio',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pib_portofolio', to='bilan.bilan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PIB',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pib_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pib_outstanding', models.FloatField()),
                ('pib_value_date', models.DateField()),
                ('pib_due_date', models.DateField()),
                ('pib_rate', models.FloatField()),
                ('pib_type', models.IntegerField(choices=[(0, 'Intrabanque'), (1, 'Interbanque')], default=0)),
                ('pib_notation', models.CharField(max_length=1)),
                ('pib_warranty', models.CharField(max_length=100)),
                ('pib_bond_number', models.IntegerField(default=0)),
                ('pib_interest', models.FloatField()),
                ('pib_cashflows', models.JSONField(default=dict)),
                ('pib_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pib_portofolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pib', to='pib.pibportofolio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
