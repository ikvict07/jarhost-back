import json
import requests

from django.http import JsonResponse, Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from jars.models import Jar
from jars.serializers import JarSerializer


@api_view(['POST'])
def AddJar(request):
    monoid = request.data['monoid']
    monoJarid = request.data['monoJarid']
    url = request.data['url']
    list_of_jars = getJarsById(monoid)
    for jar in list_of_jars:
        if jar['id'] == monoJarid:
            saveJarToDB(jar, monoid, url)
            return Response({"message": "ok", "monoid": monoid, "monoJarid": monoJarid, "jar": jar}, status=201)
    return Http404("No jar was found")

    # serializer = JarSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=201)
    # return Response(serializer.errors, status=400)
    #


@api_view(['GET'])
def JarDetail(request, pk):
    try:
        jar = Jar.objects.get(pk=pk)
    except Jar.DoesNotExist:
        raise Http404('Jar does not exist')

    jar_list = getJarsById(jar.monoid)
    for jar_from_api in jar_list:
        if jar_from_api['id'] == jar.monoJarid:
            return JsonResponse({
                "name": jar.name,
                "description": jar.description,
                "currencyCode": jar_from_api['currencyCode'],
                "balance": jar_from_api['balance'],
                "goal": jar_from_api['goal'],
                "url": jar.url
            })

    serializer = JarSerializer(jar)
    return Response(serializer.data)


@api_view(['GET'])
def FetchByUserId(request):
    return JsonResponse({"message": "mock data"})  # TODO:


def getJarsById(monoid):

    url = 'https://api.monobank.ua/personal/client-info'
    headers = {
        'X-Token': monoid,
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        monobank_data = response.json()
        jars_list = monobank_data['jars']
        return jars_list
    else:
        return None


def saveJarToDB(jar, monoid, url):
    jar_to_save = Jar()

    jar_to_save.monoid = monoid
    jar_to_save.monoJarid = jar["id"]
    jar_to_save.name = jar["title"]
    jar_to_save.description = jar["description"]
    jar_to_save.url = url

    jar_to_save.save()
