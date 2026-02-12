from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'roll_number', 'branch', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'STUDENT'
        if commit:
            user.save()
        return user
