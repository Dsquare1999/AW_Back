# Generated by Django 5.0.3 on 2024-04-11 08:07

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
            name='RefiPortofolio',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refi_portofolio', to='bilan.bilan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Refi',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('refi_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('refi_label', models.CharField(max_length=100)),
                ('refi_outstanding', models.FloatField()),
                ('refi_value_date', models.DateField()),
                ('refi_due_date', models.DateField()),
                ('refi_rate', models.FloatField()),
                ('refi_type', models.IntegerField(choices=[(0, 'Guichet des avances intra-journalières '), (1, 'Guichet spécial de refinancement'), (2, 'Guichet de prêt marginal')], default=0)),
                ('refi_interest', models.FloatField()),
                ('refi_cashflows', models.JSONField(default=dict)),
                ('refi_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('refi_portofolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refi', to='refi.refiportofolio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
