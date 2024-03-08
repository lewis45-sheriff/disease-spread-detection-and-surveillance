from django import forms
from authentication.models import CustomUser
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('healthcareworker', 'Healthcare Worker'),
    )
    
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role'] 


class DiseasePredictionForm(forms.Form):
    population_density = forms.FloatField(label='Population Density')
    reported_cases = forms.FloatField(label='Reported Cases')
from django import forms

