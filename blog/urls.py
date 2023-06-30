from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list),
    path('post/<int:pk>/', views.post_detail),
    path('post/new/', views.post_create),
    path('post/<int:pk>/edit/', views.post_update),
    path('post/<int:pk>/delete/', views.post_delete),
]
