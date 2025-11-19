from django.db import models
from django.contrib.auth.models import User



class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    skills = models.CharField(max_length=20)
    work_experience = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    service_rate = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')


class Service(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.IntegerField()

    def __str__(self):
        return self.title
    

class Message(models.Model):
    booking = models.ForeignKey('consumer.Booking', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

