from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.view_post, name='post'),
    path('create/', views.create_post_form, name='create_post_form'),
    path('create_post/', views.create_post, name='create_post'),
    path('<int:post_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]