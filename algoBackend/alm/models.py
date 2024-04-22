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


class BondPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="bond_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bond(CreateUpdateModel, models.Model):

    PERIODS = (
        ('T', 'Trimestrial'),
        ('S', 'Semestrial'),
        ('A', 'Annual')
    )

    REFUNDS = (
        ('IF', 'In Fine'),
        ('AC', 'Constant Amortissable'),
        ('ACD', 'Differed Constant Amortissable')
    )

    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portofolio = models.ForeignKey(BondPortofolio, related_name="bond", on_delete=models.CASCADE)

    isin = models.CharField(max_length=255)

    outstanding = models.FloatField() # Encours (in millions)
    issuer = models.CharField(max_length=100)
    value_date = models.DateField()
    due_date = models.DateField()
    facial_rate = models.FloatField()
    refund = models.CharField(max_length=5, choices=REFUNDS, default='IF')
    differed = models.IntegerField() # Neither in year nor in month
    refinancing = models.CharField(max_length=100)
    guarantee = models.CharField(max_length=100)
    total_number = models.IntegerField()
    number_available = models.IntegerField()
    type = models.CharField(max_length=50)
    period = models.CharField(max_length=1, choices=PERIODS, default='A')
    cotation = models.CharField(max_length=50)
    reference_value = models.FloatField(default=0)

    annual_coupon = models.FloatField(blank=True, null=True) 
    cashflows = models.JSONField(default=dict)
    valorisations = models.JSONField(default=dict)
    duration_macaulay = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.isin} {self.user}"
