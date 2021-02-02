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

  def save(self, commit=True):
    user = User.objects.create_user(
      firstname=self.cleaned_data['firstname'],
      login=self.cleaned_data['login'],
      password=self.cleaned_data['password1']
    )
    lastname = self.cleaned_data['lastname']
    if lastname:
      user.last_name = lastname
      user.save()
    
    print(user)
