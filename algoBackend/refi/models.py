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

class RefiPortofolio(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, related_name="refi_portofolio", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Refi(CreateUpdateModel, models.Model):

    TYPES = (
        (0, 'Guichet des avances intra-journalières '),
        (1, 'Guichet spécial de refinancement'),
        (2, 'Guichet de prêt marginal')
    )

    refi_id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    refi_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    refi_portofolio =  models.ForeignKey(RefiPortofolio, related_name="refi", on_delete=models.CASCADE)

    refi_label = models.CharField(max_length=100)
    refi_outstanding = models.FloatField()
    refi_value_date = models.DateField()
    refi_due_date = models.DateField()

    refi_rate = models.FloatField()
    refi_type = models.IntegerField(choices=TYPES, default=0)
    
    refi_interest = models.FloatField()
    refi_cashflows = models.JSONField(default=dict)

    def __str__(self):
        return self.refi_label + "_" + self.refi_outstanding