import requests

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from jars.models import Jar


@api_view(['POST'])
def AddJar(request):
    monoid = request.data['monoid']
    monoJarid = request.data['monoJarid']
    list_of_jars = getJarsById(monoid)

    if list_of_jars is None:
        return Response({"errors": ["Invalid monoid"]})

    for jar in list_of_jars:
        if jar['id'] == monoJarid:
            try:
                saveJarToDB(jar, monoid)
            except IntegrityError:
                return Response({"errors": ["Jar with this id already exists"]})

            return Response(jar)
    return Response({"errors": ["No jar was found"]})


@api_view(['GET'])
def JarDetail(request, pk):
    try:
        jar = Jar.objects.get(pk=pk)
    except Jar.DoesNotExist:
        return Response({"errors": ["No jar was found"]})

    jar_list = getJarsById(jar.monoid)
    for jar_from_api in jar_list:
        if jar_from_api['id'] == jar.monoJarid:
            return JsonResponse({
                "name": jar.name,
                "description": jar.description,
                "url": "https://send.monobank.ua/" + jar_from_api["sendId"],
                "currencyCode": jar_from_api['currencyCode'],
                "balance": jar_from_api['balance'],
                "goal": jar_from_api['goal'],
            })
    return Response({"errors": ["No jar was found"]})


@api_view(['GET'])
def FetchByUserId(request, pk):
    return JsonResponse({"message": "mock data"})  # TODO: implement controller


@api_view(["GET"])
def PaginationController(request):
    jars_count_in_db = len(Jar.objects.all())

    from_index = int(request.GET.get('from', 1))
    to_index = int(request.GET.get('to', jars_count_in_db))

    from_index = 1 if from_index == 0 else from_index

    jars = Jar.objects.all()[from_index - 1:to_index]
    serialized_jars = list(jars.values())

    return JsonResponse(serialized_jars, safe=False)


def getJarsById(monoid):

    url = 'https://api.monobank.ua/personal/client-info'
    headers = {
        'X-Token': monoid,
    }

    response = requests.get(url, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        monobank_data = response.json()
        jars_list = monobank_data['jars']
        return jars_list
    else:
        return None


def saveJarToDB(jar, monoid):
    jar_to_save = Jar()

    jar_to_save.monoid = monoid
    jar_to_save.monoJarid = jar["id"]
    jar_to_save.name = jar["title"]
    jar_to_save.description = jar["description"]

    jar_to_save.save()
