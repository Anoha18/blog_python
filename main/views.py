from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from account.models import User
from .forms import SignUpForm

def index(request):
  return render(request, 'main/pages/index.html')

def login(request):
  return render(request, 'main/pages/login.html')

def register(request):
  registerFormPath = 'main/pages/register.html'
  if request.method == 'GET':
    return render(request, registerFormPath)
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      print('HERE 1')
      form.save()
      login = form.cleaned_data['login']
      password = form.cleaned_data['password1']
      user = authenticate(login=login, password=password)
      login(request, user)
      return redirect('home')
    return render(request, registerFormPath, { 'errors': form.errors })
    

