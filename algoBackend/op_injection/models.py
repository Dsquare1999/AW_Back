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

class OPInjectionPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="op_injection_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OPInjection(CreateUpdateModel, models.Model):

    TYPES = (
        (0, 'Opération d\'injection liquidité de maturité longue'),
        (1, 'Opération principal d\'injection de liquidité')
    )

    op_injection_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    op_injection_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    op_injection_portofolio =  models.ForeignKey(OPInjectionPortofolio, related_name="op_injection", on_delete=models.CASCADE)

    op_injection_lender = models.CharField(max_length=100) 
    op_injection_outstanding = models.FloatField()

    op_injection_value_date = models.DateField()
    op_injection_due_date = models.DateField()

    op_injection_rate = models.FloatField()
    op_injection_type = models.IntegerField(choices=TYPES, default=0)
    
    op_injection_interest = models.FloatField()
    op_injection_cashflows = models.JSONField(default=dict)

    def __str__(self):
        return self.op_injection_lender + "_" + self.op_injection_outstanding