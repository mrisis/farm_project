from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    password1=forms.CharField(max_length=100 , widget=forms.PasswordInput)
    password2 = forms.CharField( max_length=100 , widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['mobile_number',]

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2'] :
            raise ValidationError('password dont match')
        return cd['password2']

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserchangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\"../password/\" >this form</a>')
    class Meta:
        model = User
        fields = ['mobile_number','password']