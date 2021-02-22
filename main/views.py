from django.db.models.expressions import OuterRef, Subquery
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.contrib.auth import login as Login, authenticate
from account.models import User
from .models import Post, Post_views, Comment
from .forms import SignUpForm
from account.save_user_session import SaveUserSession
from django.db.models.aggregates import Count
from markdown import Markdown
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.postgres.aggregates import ArrayAgg

md = Markdown()

def index(request):
  posts = Post.objects \
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
    .filter(deleted=False) \
    .order_by('-created_at')
  for post in posts:
      post.body = md.convert(post.body)
  return render(request, 'main/pages/index.html', { 'posts': posts })

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

def post(request, post_id):
  post = None
  try:
    post = Post.objects \
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
      .get(pk=post_id)
  except ObjectDoesNotExist:
    return Http404()
  post.body = md.convert(post.body)
  session_key = request.session.session_key

  comments = Comment.objects.filter(post_id=post_id)
  if comments is not None and len(comments) > 0:
    for comment in comments:
      comment.text = md.convert(comment.text)
    setattr(post, 'comments', comments)
  else:
    setattr(post, 'comments', [])

  if session_key is not None:
    existsView = None
    try:
      existsView = Post_views.objects.get(session_id=session_key, post_id=post_id)
    except ObjectDoesNotExist:
      existsView = None

    if existsView is None or existsView.id is None:
      Post_views.objects.create(
        session=Session.objects.get(session_key=session_key),
        post=post
      )

  return render(request, 'main/pages/post.html', { 'post': post })

@login_required
def comment(request):
  if request.method != 'POST':
    return HttpResponseBadRequest()

  if request.user.id is None:
    return HttpResponse('User not found')

  user = request.user
  comment_text = request.POST.get('commentText', None)
  post_id = request.POST.get('postId', None)
  parent_id = request.POST.get('parentId', None) or None
  if comment_text is None: return HttpResponse('Comment is empty')

  if post_id is None: return HttpResponse('Post id not found')

  try:
    Comment.objects.create(
      text=comment_text,
      creator=User.objects.get(pk=user.id),
      parent_id=parent_id,
      post=Post.objects.get(pk=post_id),
    )
  except ObjectDoesNotExist:
    return HttpResponseServerError('На сервере произошла ошибка.')
  except IntegrityError:
    return HttpResponseServerError('При сохраненни комментария произошла ошибка.')

  return redirect(f'/posts/{post_id}')