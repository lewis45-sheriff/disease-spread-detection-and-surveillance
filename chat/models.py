from django.db import models
from authentication.models import CustomUser
from django.utils import timezone

class ChatMessage(models.Model):
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="+")
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.message
