from django.shortcuts import render
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
    return render(request, registerFormPath, { 'errors': form.errors })
    

