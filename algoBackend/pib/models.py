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

class PIBPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="pib_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PIB(CreateUpdateModel, models.Model):

    TYPES = (
        (0, 'Intrabanque'),
        (1, 'Interbanque')
    )

    pib_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    pib_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pib_portofolio =  models.ForeignKey(PIBPortofolio, related_name="pib", on_delete=models.CASCADE)

    pib_outstanding = models.FloatField()
    pib_value_date = models.DateField()
    pib_due_date = models.DateField()

    pib_rate = models.FloatField()
    pib_type = models.IntegerField(choices=TYPES, default=0)
    pib_notation = models.CharField(max_length=1)
    pib_warranty = models.CharField(max_length=100)
    pib_bond_number = models.IntegerField(default=0)
    
    pib_interest = models.FloatField()
    pib_cashflows = models.JSONField(default=dict)

    def __str__(self):
        return self.pib_type + "_" + self.pib_outstanding