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

class DATPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="dat_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DAT(CreateUpdateModel, models.Model):
    PERIODS = (
        ('M', 'Monthly'),
        ('T', 'Trimestrial'),
        ('S', 'Semestrial'),
        ('A', 'Annual')
    )

    TYPES = (
        (0, 'Type 1'),
        (1, 'Type 2')
    )

    dat_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    dat_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dat_portofolio =  models.ForeignKey(DATPortofolio, related_name="dat", on_delete=models.CASCADE)

    dat_client = models.CharField(max_length=100)
    dat_outstanding = models.FloatField()
    dat_value_date = models.DateField()
    dat_due_date = models.DateField()

    dat_period = models.CharField(max_length=1, choices=PERIODS, default=0)
    dat_rate = models.FloatField()
    dat_type = models.CharField(max_length=100, choices=TYPES, default=0)

    dat_interest = models.FloatField()
    dat_cashflows = models.JSONField(default=dict)

    def __str__(self):
        return self.dat_client + "_" + self.dat_outstanding