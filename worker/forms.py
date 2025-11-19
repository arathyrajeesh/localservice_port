from django import forms
from django.contrib.auth.models import User
from .models import Worker,Service

class WorkerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['phone', 'skills', 'service_rate', 'work_experience', 'city']



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'experience']
