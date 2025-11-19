from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ConsumerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey('worker.Service', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.consumer.username}"
