from django.shortcuts import render

def index(request):
  return render(request, 'main/pages/index.html')

def login(request):
  return render(request, 'main/pages/login.html')
