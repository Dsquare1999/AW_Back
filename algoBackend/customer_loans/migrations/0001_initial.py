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
            name='CustomerLoanPortofolio',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_loan_portofolio', to='bilan.bilan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerLoan',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('loan_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('loan_borrower', models.CharField(max_length=100)),
                ('loan_period', models.CharField(choices=[('M', 'Monthly'), ('T', 'Trimestrial'), ('S', 'Semestrial'), ('A', 'Annual')], default='A', max_length=1)),
                ('loan_outstanding', models.FloatField()),
                ('loan_value_date', models.DateField()),
                ('loan_due_date', models.DateField()),
                ('loan_rate', models.FloatField()),
                ('loan_status', models.CharField(max_length=100)),
                ('loan_refund', models.CharField(max_length=100)),
                ('loan_type', models.CharField(choices=[('Particuliers', 'Particuliers'), ('Entreprises Publiques', 'Entreprises Publiques'), ('Entreprises Privées', 'Entreprises Privées'), ('Autres', 'Autres')], default='Particuliers', max_length=100)),
                ('loan_interest', models.FloatField()),
                ('loan_cashflows', models.JSONField(default=dict)),
                ('loan_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loan_portofolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_loan', to='customer_loans.customerloanportofolio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
