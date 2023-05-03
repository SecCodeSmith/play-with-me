import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.backends.db import SessionStore
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import authentication_classes, api_view, permission_classes

from api.models import USER
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def index(request):
    respond = {'Mess': "This is the api."}
    return JsonResponse(respond)


@api_view(['POST'])
def login(request):
    username = request.POST.get('login')
    password = request.POST.get('password')

@api_view(['POST'])
def register(request):
    username = request.POST.get('login')
    password = request.POST.get('password')


