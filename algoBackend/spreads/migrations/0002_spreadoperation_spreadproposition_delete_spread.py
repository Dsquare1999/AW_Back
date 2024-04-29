# Generated by Django 5.0.3 on 2024-04-29 11:37

import django.contrib.postgres.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0004_adminbond_country'),
        ('spreads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpreadOperation',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bid', models.FloatField()),
                ('ask', models.FloatField()),
                ('adviced_bid', models.FloatField(blank=True, null=True)),
                ('adviced_ask', models.FloatField(blank=True, null=True)),
                ('spread', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('order', models.IntegerField(choices=[(0, 'Minimum Volume Order'), (1, 'Volume Available Order'), (2, 'All or None Order'), (3, 'Complex Order')], default=0)),
                ('type', models.CharField(choices=[('B', 'Buy'), ('S', 'Sell')], default='B', max_length=10)),
                ('validity', models.DateField()),
                ('attractive', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=list, size=5)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('isPublic', models.BooleanField(default=True)),
                ('isPublished', models.BooleanField(default=True)),
                ('admin_bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.adminbond')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpreadProposition',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('volume', models.IntegerField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P', max_length=50)),
                ('confirmation', models.BooleanField(default=False)),
                ('accepted_date', models.DateField(blank=True, null=True)),
                ('confirmation_date', models.DateField(blank=True, null=True)),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propositions', to='spreads.spreadoperation')),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Spread',
        ),
    ]
