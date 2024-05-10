import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

from accounts.models import User
from alm.models import Bond

# Create your models here.

class CreateUpdateModel(models.Model):
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta : 
        abstract = True

class SwapOperation(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    offer = models.ForeignKey(Bond, on_delete=models.CASCADE)
    offer_duration = models.FloatField(default=0.0)
    offer_quantity = models.IntegerField(default=0)
    offer_return = models.FloatField(default=0.0)
    offer_country = models.CharField(max_length=100, blank=True, null=True)

    validity = models.DateField()

    demand_duration = models.FloatField(default=0.0)
    demand_quantity = models.IntegerField(default=0)
    demand_return = models.FloatField(default=0.0)
    demand_country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.offer)

class SwapProposition(CreateUpdateModel, models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    operation = models.ForeignKey(SwapOperation, related_name="propositions", on_delete=models.CASCADE)
    proposer = models.ForeignKey(User, on_delete=models.CASCADE)
    proposition = models.ForeignKey(Bond, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default='P')
    accepted_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.operation) + " " + str(self.proposer)