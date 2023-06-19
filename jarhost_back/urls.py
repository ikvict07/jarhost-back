from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/jars/', include('jars.urls')),
    path('auth/', include('authentication.urls')),
]
