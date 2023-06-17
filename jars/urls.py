from django.urls import path

from jars.views import AddJar, JarDetail, FetchByUserId, PaginationController

urlpatterns = [
    path('add/', AddJar),
    path('<int:pk>/', JarDetail),
    path('fetch-by-user-id/<int:pk>', FetchByUserId),
    path('', PaginationController),
]
