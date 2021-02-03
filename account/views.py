from django.shortcuts import redirect, render
from django.contrib.auth import logout as Logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
  return render(request, 'account/pages/index.html')

@login_required
def logout(request):
  Logout(request)
  return redirect('home')