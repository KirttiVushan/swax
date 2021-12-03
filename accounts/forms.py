from django.forms import fields
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm



class CreateUserForm(UserCreationForm):
    
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address")

    class Meta:
        model = CustomUser
        fields = ('email','password1','password2')







