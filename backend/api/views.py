import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.models import USER as user


def index(request):
    respond = {'Mess': "This is the api."}
    return JsonResponse(respond)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)



