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

class OPRetraitPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="op_retrait_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OPRetrait(CreateUpdateModel, models.Model):

    TYPES = (
        (0, 'Bond BCEAO'),
        (1, 'Retrait')
    )

    op_retrait_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    op_retrait_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    op_retrait_portofolio = models.ForeignKey(OPRetraitPortofolio, related_name="op_retrait", on_delete=models.CASCADE)

    op_retrait_lender = models.CharField(max_length=100) 
    op_retrait_outstanding = models.FloatField()

    op_retrait_value_date = models.DateField()
    op_retrait_due_date = models.DateField()

    op_retrait_rate = models.FloatField()
    op_retrait_type = models.IntegerField(choices=TYPES, default=0)
    
    op_retrait_interest = models.FloatField()
    op_retrait_cashflows = models.JSONField(default=dict)

    def __str__(self):
        return self.op_retrait_lender + "_" + self.op_retrait_outstanding