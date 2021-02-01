from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from account.models import User

class SignUpForm(UserCreationForm):
  firstname = forms.CharField(help_text='Обязательное поле', required=True)
  lastname = forms.CharField(help_text='Обязательное поле', required=False)
  login = forms.CharField(help_text='Обязательное поле', required=True)
  password1 = forms.CharField(help_text='Обязательное поле', required=True)
  password2 = forms.CharField(help_text='Обязательное поле', required=True)

  class Meta:
    model = User
    fields = ('firstname', 'lastname', 'login', 'password1', 'password2')