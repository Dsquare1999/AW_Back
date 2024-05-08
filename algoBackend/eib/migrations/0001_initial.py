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
            name='EIBPortofolio',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eib_portofolio', to='bilan.bilan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EIB',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('eib_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('eib_lender', models.CharField(max_length=100)),
                ('eib_effect', models.IntegerField(choices=[(0, 'Pension'), (1, 'A Blanc')], default=0)),
                ('eib_outstanding', models.FloatField()),
                ('eib_value_date', models.DateField()),
                ('eib_due_date', models.DateField()),
                ('eib_rate', models.FloatField()),
                ('eib_type', models.IntegerField(choices=[(0, 'Intrabanque'), (1, 'Interbanque')], default=0)),
                ('eib_warranty', models.CharField(max_length=100)),
                ('eib_bond_number', models.IntegerField(default=1)),
                ('eib_interest', models.FloatField()),
                ('eib_cashflows', models.JSONField(default=dict)),
                ('eib_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('eib_portofolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eib', to='eib.eibportofolio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
