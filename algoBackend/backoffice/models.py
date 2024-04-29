import uuid
from django.db import models

# Create your models here.

class CreateUpdateModel(models.Model):
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta : 
        abstract = True

class AdminBond(CreateUpdateModel, models.Model):

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

    SPACES = (
        ('CEDEAO', 'Communauté Economique des Etats de l\'Afrique de l\'Ouest (CEDEAO)'),
        ('CEMAC', 'Communauté économique et monétaire de l\'Afrique centrale (CEMAC)'),
        ('COMORES', 'Union des Comores (UC)'),
        ('UEAC', 'Union des États de l\'Afrique centrale (UEAC)'),
        ('UA', 'Union africaine (UA)')
    )

    ENTITIES = (
        ('Country', 'Country'),
        ('Society', 'Society'),
    )

    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    isin = models.CharField(max_length=255, unique=True)

    country = models.CharField(max_length=100)
    space = models.CharField(max_length=255, choices=SPACES, default='UEMOA')
    description = models.TextField(default='')
    entity = models.CharField(max_length=20, choices = ENTITIES, default = 0)

    due_date = models.DateField()
    facial_rate = models.FloatField()
    refund = models.CharField(max_length=5, choices=REFUNDS, default='IF')
    differed = models.IntegerField() # Neither in year nor in month

    guarantee = models.CharField(max_length=100)
    total_number = models.IntegerField()
    type = models.CharField(max_length=50)
    period = models.CharField(max_length=1, choices=PERIODS, default='A') 

    def __str__(self):
        return "Admin " + self.isin