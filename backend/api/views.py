import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from api.models import USER as user
from rest_framework.response import Response



@api_view(['POST'])
def index(request):
    respond = {'Mess': "This is the api."}
    return JsonResponse(respond)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])

    if user is not None:
        # User credentials are valid
        return Response({'status': 'Login successful'})
    else:
        # User credentials are invalid
        return Response({'status': 'Login failed'}, status=401)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)



def get_csrf_token(request):
    # Generate CSRF token
    csrf_token = get_token(request)

    # Return the token in a JSON response
    return JsonResponse({'csrf_token': csrf_token})
