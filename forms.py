from django import forms
from med_alert_app.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UploadFileForm(forms.Form):
    file = forms.FileField()