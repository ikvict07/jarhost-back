import re
import requests
from .models import CustomUser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']

        if CustomUser.objects.filter(username=username).exists():
            return Response({'errors': ['Username already exists']}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({'errors': ['Password is too short (min 6 chars)']}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(username) < 3:
            return Response({'errors': ['Username is too short (min 3 chars)']}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validate_email(email):
            return Response({'errors': ['Invalid email']}, status=status.HTTP_400_BAD_REQUEST)


        user = CustomUser(username=username, password=make_password(password), email=email)
        user.save()

        return Response({"message": "User has been created"}, status=status.HTTP_201_CREATED)

    except KeyError:
        return Response({"errors": ["Please provide all fields"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'Invalid username/password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not user.check_password(password):
        return Response(
            {'error': 'Invalid username/password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate(request):
    data = request.data
    monoid = request.data['monoid']

    url = 'https://api.monobank.ua/personal/client-info'
    headers = {
        'X-Token': monoid,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == status.HTTP_200_OK:
        email = EmailMessage(
            'Subject',  # Тема письма
            'Body',  # Тело письма
            'jarhost@ukr.net',  # Отправитель
            ['yaroslavtok.work@gmail.com'],  # Список получателей
            headers={'Message-ID': 'foo'},  # Заголовки письма
        )
        email.send()

    return Response({"message": f"{response.status_code}"}, status=status.HTTP_200_OK)




def validate_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if re.match(email_regex, email):
        return True
    else:
        return False
