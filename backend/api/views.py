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
    else:
        return JsonResponse({'status': 'Accepted only post'})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'status': 'Logout success.'})
    return JsonResponse({'status': 'Logout failed'})


def register(request):
    respond = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password1')
        if data.get('password1') != data.get('password2'):
            respond['password'] = "Passwords are not identical."
        if usr.objects.filter(email=email).exists():
            respond['email'] = "Email is already in use."
        if usr.objects.filter(username=username).exists():
            respond['username'] = "Username is already in use."

        language = lang.get_lang(data.get('language'))

        if len(respond) > 0:
            respond['status'] = "Create new user fail"
            return JsonResponse(respond)

        if usr.objects.create_user(username=username, password=password, email=email, lang=language):
            respond['status'] = "Create new user success"
        else:
            respond['status'] = "Create new user fail"
        return JsonResponse(respond)
    else:
        return JsonResponse({'status': 'Accepted only POST'})


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
    respond = {l.name: {'ISO_639_1': l.ISO_639_1, 'ISO_639_2': l.ISO_639_2} for l in language}
    return JsonResponse(respond)


def get_lang(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        ISO_639_1 = data.get('ISO_639_1')
        ISO_639_2 = data.get('ISO_639_2')
    if request.method == 'GET':
        name = request.GET.get('name')
        ISO_639_1 = request.GET.get('ISO_639_1')
        ISO_639_2 = request.GET.get('ISO_639_2')

    if not (request.method == 'GET' or request.method == 'POST'):
        return JsonResponse({'status': 'Accepted POST and GET'})
    language = lang.objects.filter(name=name) if name else lang.objects.filter(
        ISO_639_1=ISO_639_1) if ISO_639_1 else lang.objects.filter(
        ISO_639_2=ISO_639_2) if ISO_639_2 else lang.objects.all()
    respond = {l.name: {'ISO_639_1': l.ISO_639_1, 'ISO_639_2': l.ISO_639_2} for l in language}
    return JsonResponse(respond)


def user_set_description(request):
    data = json.loads(request.body)
    usr.description = data['description']
    usr.save()
    return JsonResponse({'status': "success"})
