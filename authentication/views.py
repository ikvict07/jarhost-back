import re
import requests
from .models import CustomUser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

MIN_LASTNAME_LEN = 1

MIN_FIRSTNAME_LEN = 1

MIN_USERNAME_LEN = 3

MIN_PASSWORD_LEN = 6


@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    try:
        first_name = request.data['firstName']
        last_name = request.data['lastName']
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']

        if CustomUser.objects.filter(username=username).exists():
            return Response({'errors': ['Username already exists']})

        if len(password) < MIN_PASSWORD_LEN:
            return Response({'errors': ['Password is too short (min 6 chars)']})

        if len(username) < MIN_USERNAME_LEN:
            return Response({'errors': ['Username is too short (min 3 chars)']})

        if not validate_email(email):
            return Response({'errors': ['Invalid email']})

        if len(first_name) <= MIN_FIRSTNAME_LEN:
            return Response({'errors': ['First name is too short']})

        if len(last_name) <= MIN_LASTNAME_LEN:
            return Response({'errors': ['Last name is too short']})

        user = CustomUser(
            username=username,
            password=make_password(password),
            email=email, first_name=first_name,
            last_name=last_name)
        user.save()

        return Response({"message": "User has been created"})

    except KeyError:
        return Response({"errors": ["Please provide all fields"]})


@api_view(['POST'])
@permission_classes([AllowAny])
def LogIn(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'errors': ['Invalid username/password']})

    if not user.check_password(password):
        return Response({'errors': ['Invalid username/password']})

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Validate(request):
    try:
        monoid = request.data['monoid']
        message = request.data['message']
        telegram = request.data['telegram']
    except KeyError:
        return Response({'errors': ['Please provide all fields']})

    url = 'https://api.monobank.ua/personal/client-info'
    headers = {
        'X-Token': monoid,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == status.HTTP_200_OK:
        send_message_to_tg(monoid, message, telegram, request.user)
        return Response({"message": "Your data was successfully sent to the administrator "})
    else:
        return Response({"errors": ["Invalid monoid"]})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchCurrentUser(request):
    return Response(
        {
            "firstName": request.user.first_name,
            "lastName": request.user.last_name,
            "email": request.user.email,
            "photo": request.user.photo,
            "about": request.user.about,
            "isFundraiser": request.user.isFundraiser
        }
    )


def validate_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email)


def send_message_to_tg(monoid, message, telegram, request_user):
    bot_token = '<your-token>'
    bot_chatID = '<your-chatID>'

    bot_message = f"""
❗❗❗Нова заявка на верифікацію❗❗❗:
Telegram: {telegram}
MonoId: {monoid}
Ім'я: {request_user.first_name}
Прізвище: {request_user.last_name}
Email: {request_user.email}`
Повідомлення: {message}      
    """
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' +\
                bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response
