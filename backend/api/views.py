import json

from django.contrib.auth import login as log, logout, authenticate
from django.http import JsonResponse
from django.middleware.csrf import get_token
from api.models import USER as usr, LANGUAGE as lang


def index(request):
    respond = {'Mess': "This is the api."}
    if request.user.is_authenticated:
        respond['LoginStatus'] = True
    return JsonResponse(respond)


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
    if user is not None:
        log(request, user)
        # User credentials are valid
        return JsonResponse({'status': 'Login successful'})
    else:
        # User credentials are invalid
        return JsonResponse({'status': 'Login failed'})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'status': 'Logout success.'})
    return JsonResponse({'status': 'Logout failed'})


def register(request):
    respond = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        username = data['username']
        password = data['password1']
        if data['password1'] == data['password2']:
            request['password'] = "Passwords are not identical."
        if usr.objects.get(email=email) is not None:
            request['email'] = "Email is already in use."
        if usr.objects.get(username=username):
            request['email'] = "Username is already in use."
        language = lang.objects.get(data['language'])
        if language is None:
            request['language'] = "Language don't exist."
        if len(respond) > 0:
            respond['status'] = "Create new user fail"
            return JsonResponse(respond)

        if usr.create_user(username, password, email, language):
            respond['status'] = "Create new user success"
        else:
            respond['status'] = "Create new user fail"
        return JsonResponse(respond)


def is_auth_session(request):
    respond = {}
    if request.user.is_authenticated:
        respond['LoginStatus'] = True
        respond['username'] = request.user.username
    else:
        respond['LoginStatus'] = False
    return JsonResponse(respond)


def get_csrf_token(request):
    # Generate CSRF token
    csrf_token = get_token(request)

    # Return the token in a JSON response
    return JsonResponse({'csrf_token': csrf_token})


def get_lang_list(request):
    language = lang.objects.all()
    respond = {l.crosscut: l.name for l in language}
    return JsonResponse(respond)


def user_set_description(request):
    data = json.loads(request.body)
    usr.description = data['description']
