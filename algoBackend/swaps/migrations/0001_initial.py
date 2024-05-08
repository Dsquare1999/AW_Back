# Generated by Django 5.0.3 on 2024-05-07 09:55

import django.contrib.postgres.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SwapOperation',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('validity', models.DateField()),
                ('attractive', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=list, size=5)),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alm.bond')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SwapProposition',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(default='P', max_length=1)),
                ('accepted_date', models.DateField(blank=True, null=True)),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propositions', to='swaps.swapoperation')),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proposition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alm.bond')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
