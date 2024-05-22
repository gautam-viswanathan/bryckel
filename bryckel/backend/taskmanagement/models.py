from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class taskManager(models.Model):
    STATUS=(('High','High'),('Medium','Medium'),('Low','Low'))
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=200)
    due_date=models.DateField()
    priority=models.CharField(max_length=200,choices=STATUS)
    status=models.BooleanField(max_length=200)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)