from django.http import JsonResponse
from django.shortcuts import render
import json

def JarHandler(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        return JsonResponse({"name": f"{body_data['name']}"})
