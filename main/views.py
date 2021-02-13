from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login as Login, authenticate
from account.models import User
from .forms import SignUpForm
from account.save_user_session import SaveUserSession

def index(request):
  return render(request, 'main/pages/index.html')

def login(request):
  redirectPage = 'main/pages/login.html'
  nextPage = request.GET.get('next');
  
  if request.user.id is not None:
    return redirect('/account')

  if request.method == 'GET':
    return render(request, redirectPage)

  if request.method == 'POST':
    _login = request.POST['login']
    password = request.POST['password']

    user = authenticate(login=_login, password=password)
    if user is None:
      return render(request, redirectPage)
    Login(request, user)
    request.session['user_id'] = user.id
    SaveUserSession(request.session.session_key, user.id)
    if nextPage is not None:
      return redirect(nextPage);
    else:
      return redirect('account_home')

  return render(request, redirectPage)

def register(request):
  registerFormPath = 'main/pages/register.html'
  if request.method == 'GET':
    return render(request, registerFormPath)
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      login = form.cleaned_data['login']
      password = form.cleaned_data['password1']
      user = authenticate(login=login, password=password)
      Login(request, user)
      request.session['user_id'] = user.id
      SaveUserSession(request.session.session_key, user.id)
      return redirect('account_home')
    return render(request, registerFormPath, { 'errors': form.errors })
    

def not_found_page(request, exception):
  return HttpResponse('Sorry. Page not found')
