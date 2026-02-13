from django import forms
from .models import JobDrive as Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['created_by', 'created_at']
