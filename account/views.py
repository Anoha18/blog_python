from datetime import datetime
from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout as Logout
from django.contrib.auth.decorators import login_required
from main.models import Category, Post
from transliterate import translit
import json
from .file_upload import file_upload
import traceback
from markdown import Markdown

@login_required
def index(request):
  return render(request, 'account/pages/index.html')

@login_required
def logout(request):
  Logout(request)
  user = request.session.get('user', None)
  if user is not None:
    del request.session['user']
  return redirect('home')

@login_required
def posts(request):
  user = request.user

  if request.method == 'GET':
    md = Markdown()
    userPosts = Post.objects.annotate(views_count=Count('post_views')).annotate(comments_count=Count('comment')).filter(creator=user.id).filter(deleted=False)
    for userPost in userPosts:
      userPost.body = md.convert(userPost.body)
    return render(request, 'account/pages/posts.html', { 'posts': userPosts })

@login_required
def new_post(request):
  user = request.user

  if request.method == 'GET':
    categories = Category.objects.all()
    return render(request, 'account/pages/new_post.html', { 'categories': categories })
  
  if request.method == 'POST':
    try:
      postImage = request.FILES['post_image']
      fileUrl = file_upload(user.id, postImage)
      postTitle = request.POST['postTitle']
      categoryId = request.POST['category_id']
      postText = request.POST['postText']

      Post.objects.create(
        title=postTitle,
        body=postText,
        image=fileUrl,
        creator=user,
        updated_at=datetime.now(),
        category=Category.objects.get(pk=int(categoryId))
      )
      return redirect('account_posts')
    except:
      print(f'Error. /new_post Error message = {traceback.format_exc()}')
      return render(request, 'account/pages/new_post.html', {
        'categories': Category.objects.all(),
        'postTitle': request.POST['postTitle'],
        'categoryId': request.POST['category_id'],
        'postText': request.POST['postText'],
        'imagePost': request.FILES['post_image'],
        'errorMessage': traceback.format_exc()
      });

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

@login_required
def category(request, cat_id):
  if request.method == 'DELETE':
    cat = Category.objects.get(pk = cat_id)
    cat.delete()
    return HttpResponse(status=200)
  
  return redirect('account_categories')
