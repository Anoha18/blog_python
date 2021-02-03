from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="account_home"),
  path('logout/', views.logout, name="account_logout")
]