import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

from accounts.models import User
from backoffice.models import AdminBond

# Create your models here.

class CreateUpdateModel(models.Model):
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta : 
        abstract = True


class SpreadOperation(CreateUpdateModel, models.Model):
    ORDERS = (
        (0, 'Minimum Volume Order'),
        (1, 'Volume Available Order'),
        (2, 'All or None Order'),
        (3, 'Complex Order'),
    )

    TYPE = (
        ('B', 'Buy'),
        ('S', 'Sell'),
    )

    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin_bond = models.ForeignKey(AdminBond, on_delete=models.CASCADE)

    bid = models.FloatField()
    ask = models.FloatField()
    adviced_bid = models.FloatField(blank=True, null=True)
    adviced_ask = models.FloatField(blank=True, null=True)
    spread = models.FloatField()
    quantity = models.IntegerField()
    order = models.IntegerField(choices=ORDERS, default=0)
    type = models.CharField(max_length=10, choices=TYPE, default='B')
    validity = models.DateField()
    # attractive = ArrayField(models.BooleanField(), size=5, blank=True, null=True)

    description = models.TextField(default='', blank=True, null=True)
    isPublic = models.BooleanField(default=True)
    isPublished = models.BooleanField(default=True)

    def __str__(self):
        return  "Spread Operation" + str(self.admin_bond)
    

class SpreadProposition(CreateUpdateModel, models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )

    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    operation = models.ForeignKey(SpreadOperation, related_name="propositions", on_delete=models.CASCADE)
    proposer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    volume = models.IntegerField()
    status = models.CharField(max_length=50, default='P', choices=STATUS)
    confirmation = models.BooleanField(default=False)
    accepted_date = models.DateField(blank=True, null=True)
    confirmation_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.operation) + " " + str(self.price) + " " + str(self.volume)
    