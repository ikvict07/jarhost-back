from django.urls import path
from .views import Register, LogIn, Validate, FetchCurrentUser

urlpatterns = [
    path('register/', Register),
    path('login/', LogIn),
    path('validate-user/', Validate),
    path('me/', FetchCurrentUser),
]
