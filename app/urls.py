from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
]