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

class EIBPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="eib_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EIB(CreateUpdateModel, models.Model):
    PERIODS = (
        ('M', 'Monthly'),
        ('T', 'Trimestrial'),
        ('S', 'Semestrial'),
        ('A', 'Annual')
    )

    EFFECT = (
        (0, 'Pension'),
        (1, 'A Blanc')
    )

    TYPES = (
        (0, 'Intrabanque'),
        (1, 'Interbanque')
    )

    eib_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    eib_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    eib_portofolio =  models.ForeignKey(EIBPortofolio, related_name="eib", on_delete=models.CASCADE)

    eib_lender = models.CharField(max_length=100)
    eib_effect = models.IntegerField(choices=EFFECT, default=0)
    eib_outstanding = models.FloatField()

    eib_value_date = models.DateField()
    eib_due_date = models.DateField()

    eib_rate = models.FloatField()
    eib_type = models.IntegerField(choices=TYPES, default=0)
    eib_warranty = models.CharField(max_length=100)
    eib_bond_number = models.IntegerField(default=1)
    
    eib_interest = models.FloatField()
    eib_cashflows = models.JSONField(default=dict)
    
    def __str__(self):
        return self.eib_lender