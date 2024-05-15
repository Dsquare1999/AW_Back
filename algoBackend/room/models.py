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

class Room(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='rooms', blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Message(CreateUpdateModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    def __str__(self):
        return str(self.room) + " " + str(self.user)

    class Meta:
        ordering = ('-created_at',)
