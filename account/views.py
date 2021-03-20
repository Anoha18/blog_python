from datetime import datetime
from main.views import post, register
from django.db.models.aggregates import Count
from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import logout as Logout
from django.contrib.auth.decorators import login_required
from main.models import Category, Post, Post_views, Comment
from transliterate import translit
from django.db.models.expressions import OuterRef, Subquery
import json, locale
from .file_upload import file_upload
import traceback
from markdown import Markdown
from django.db.models.functions import TruncMonth
from django.db.models import Exists

locale.setlocale(locale.LC_ALL, 'russian_russia')

@login_required
def index(request):
  user = request.user
  posts_views = (
    Post_views.objects
      .annotate(month=TruncMonth('created_at'))
      .values('month')
      .annotate(count=Count('id'))
      .filter(
        Exists(
          Post.objects.filter(pk=OuterRef('post_id'), creator=user)
        )
      )
  )
  posts_comments = (
    Comment.objects
      .annotate(month=TruncMonth('created_at'))
      .values('month')
      .annotate(count=Count('id'))
      .filter(
        Exists(
          Post.objects.filter(pk=OuterRef('post_id'), creator=user)
        )
      )
  )

  for post_view in posts_views:
    month = post_view.get('month', None)
    if month is not None:
      post_view['month'] = month.strftime('%B')

  for post_comment in posts_comments:
    month = post_comment.get('month', None)
    if month is not None:
      post_comment['month'] = month.strftime('%B')

  context = {
    'data': json.dumps(
      {
        'post_views': [
          {
            'month': post_view.get('month', None),
            'count': post_view.get('count', None)
          }
          for post_view in posts_views
        ],
        'post_comments': [
          {
            'month': post_comment.get('month', None),
            'count': post_comment.get('count', None)
          }
          for post_comment in posts_comments
        ]
      }
    )
  }
  return render(request, 'account/pages/index.html', context)

@login_required
def logout(request):
  Logout(request)
  user = request.session.get('user', None)
  if user is not None:
    del request.session['user']
  return redirect('home')

@login_required
def posts(request):
  if request.method == 'GET':
    md = Markdown()
    posts = Post.objects \
    .filter(creator=request.user) \
    .annotate(views_count=Subquery(
        Post_views.objects
          .filter(post=OuterRef('pk'))
          .values('post')
          .annotate(count=Count('pk'))
          .values('count')
      )) \
      .annotate(comments_count=Subquery(
        Comment.objects
          .filter(post=OuterRef('pk'))
          .values('post')
          .annotate(count=Count('pk'))
          .values('count')
      )) \
    .order_by('-created_at') \
    .order_by('deleted')
    # .filter(deleted=False) \
  for post in posts:
    post.body = md.convert(post.body)
    if post.views_count is None:
      post.views_count = 0
    if post.views_count > 1000:
      post.views_count = f'{round(post.views_count / 1000)}k'

  return render(request, 'account/pages/posts.html', { 'posts': posts })

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
    categories = Category.objects \
      .annotate(post_count=Count('post')) \
      .all()
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

@login_required
def edit_post(request, post_id):
  user = request.user
  post = None
  try:
    post = Post.objects.get(pk = post_id)
  except:
    return HttpResponseNotFound()

  if post is None or post.id is None:
    return HttpResponseNotFound()

  categories = Category.objects.all()

  if request.method == 'GET':
    return render(request, 'account/pages/new_post.html', {
      'categories': categories,
      'post': post,
    })

  if request.method == 'POST':
    postImage = request.FILES.get('post_image', None)
    fileUrl = None

    if postImage is not None:
      fileUrl = file_upload(user.id, postImage)

    postTitle = request.POST['postTitle']
    categoryId = request.POST['category_id']
    postText = request.POST['postText']

    post.title = postTitle
    post.body = postText
    if fileUrl is not None:
      post.image = fileUrl
    post.updated_at = datetime.now()
    post.category = Category.objects.get(pk=int(categoryId))
    post.save()
    return redirect('account_posts')

  return render(request, 'account/pages/new_post.html', { 'categories': categories, 'post': post })
