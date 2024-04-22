import uuid
from django.db import models
from accounts.models import User
from bilan.models import Bilan

# Create your models here.

class CreateUpdateModel(models.Model):
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta : 
        abstract = True

class CustomerLoanPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="customer_loan_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomerLoan(CreateUpdateModel, models.Model):
    PERIODS = (
        ('M', 'Monthly'),
        ('T', 'Trimestrial'),
        ('S', 'Semestrial'),
        ('A', 'Annual')
    )

    TYPES = (
        ('Particuliers', 'Particuliers'),
        ('Entreprises Publiques', 'Entreprises Publiques'),
        ('Entreprises Privées', 'Entreprises Privées'),
        ('Autres', 'Autres')
    )

    loan_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    loan_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_portofolio = models.ForeignKey(CustomerLoanPortofolio, related_name="customer_loan",on_delete=models.CASCADE)  

    loan_borrower = models.CharField(max_length=100)
    loan_period = models.CharField(max_length=1, choices=PERIODS, default='A')
    loan_outstanding = models.FloatField()

    loan_value_date = models.DateField()
    loan_due_date = models.DateField()

    loan_rate = models.FloatField()
    loan_status = models.CharField(max_length=100)
    loan_refund = models.CharField(max_length=100)

    loan_type = models.CharField(max_length=100, choices=TYPES, default='Particuliers')

    loan_interest = models.FloatField()
    loan_cashflows = models.JSONField(default=dict)

    def __str__(self):
        return self.loan_borrower