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
            name='OPRetraitPortofolio',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='op_retrait_portofolio', to='bilan.bilan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OPRetrait',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('op_retrait_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('op_retrait_lender', models.CharField(max_length=100)),
                ('op_retrait_outstanding', models.FloatField()),
                ('op_retrait_value_date', models.DateField()),
                ('op_retrait_due_date', models.DateField()),
                ('op_retrait_rate', models.FloatField()),
                ('op_retrait_type', models.IntegerField(choices=[(0, 'Bond BCEAO'), (1, 'Retrait')], default=0)),
                ('op_retrait_interest', models.FloatField()),
                ('op_retrait_cashflows', models.JSONField(default=dict)),
                ('op_retrait_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('op_retrait_portofolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='op_retrait', to='op_retrait.opretraitportofolio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
