from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout as Logout
from django.contrib.auth.decorators import login_required
from main.models import Category
from transliterate import translit
import json

@login_required
def index(request):
  return render(request, 'account/pages/index.html')

@login_required
def logout(request):
  Logout(request)
  return redirect('home')

@login_required
def posts(request):
  return render(request, 'account/pages/posts.html')

@login_required
def new_post(request):
  return render(request, 'account/pages/new_post.html')

@login_required
def categories(request):
  if request.method == 'GET':
    categories = Category.objects.all()
    return render(request, 'account/pages/categories.html', { 'categories': categories })
  
  if request.method == 'POST':
    try:
      body = json.loads(request.body)
      categoryName = body['categoryName']
      categoryDesc = body['categoryDesc']

      brief = translit(categoryName, 'ru', reversed=True)
      brief = brief.replace(' ', '_')
      brief = brief.upper()
      Category.objects.create(
        name=categoryName,
        description=categoryDesc,
        brief=brief
      )
      return HttpResponse(status=200)
    except Exception:
      return HttpResponse(status=500, content='Exception')
    return ;