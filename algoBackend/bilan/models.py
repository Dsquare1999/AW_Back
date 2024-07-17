import uuid
from django.db import models

from accounts.models import User

# Create your models here.

class CreateUpdateModel(models.Model):
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta : 
        abstract = True

class Bilan(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    is_simulated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_bilan_per_user'
            )
        ]
    
    def __str__(self):
        return "Bilan " + str(self.user)