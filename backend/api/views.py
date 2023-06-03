import json

from django.contrib.auth import login as log, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.middleware.csrf import get_token
from api.models import User as usr, LANGUAGE as lang, FRIENDSHIP
from datetime import date


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
    respond = {}
    if request.user.is_authenticated and request.method == 'POST':
        data = json.loads(request.body)
        user = usr.objects.get(pk=request.user.pk)
        user.description = data['description']
        user.save()
        respond['status'] = True
        respond['mess'] = 'User description updated.'
        respond['description'] = data['description']
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'

    return JsonResponse(respond)


def change_password(request):
    respond = {}
    if request.user.is_authenticated and request.method == 'POST':
        data = json.loads(request.body)
        password = data['password']
        new_password1 = data['new_password1']
        new_password2 = data['new_password2']
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user = usr.objects.get(pk=request.user.pk)
            if new_password1 == new_password2:
                user.password = make_password(new_password1)
                user.save()
                respond['status'] = True
                respond['mess'] = 'User password updated.'
            else:
                respond['status'] = False
                respond['mess'] = 'Fail passwords are not the same.'
        else:
            respond['status'] = False
            respond['mess'] = 'Not a valid password.'

    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)


def add_friendship(request):
    respond = {}
    if request.user.is_authenticated and request.method == 'POST':
        data = json.loads(request.body)
        user1 = usr.objects.get(pk=request.user.pk)
        pk2 = data.get('pk')
        username = data.get('username')
        if pk2 is not None:
            try:
                user2 = usr.objects.get(pk=pk2)
            except usr.DoesNotExist:
                user2 = None

        if username is not None and user2 is not None:
            try:
                user2 = usr.objects.get(username=username)
            except FRIENDSHIP.DoesNotExist:
                user2 = None
        if user2 is None:
            respond['status'] = False
            respond['mess'] = 'User don\'t found.'
            return JsonResponse(respond)
        if user1.pk == user2.pk:
            respond['status'] = False
            respond['mess'] = 'You can\'t invite to friend yourself.'
        else:
            FRIENDSHIP.objects.create(create_date=date.today(), user1=user1, user2=user2).save()
            respond['status'] = True
            respond['mess'] = 'Invition sent.'
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)


def active_friendship_invite(request):
    respond = {}
    if request.user.is_authenticated and request.method == 'POST':

        try:
            list = FRIENDSHIP.objects.filter(user2=request.user, active=False)
        except FRIENDSHIP.DoesNotExist:
            list = []

        respond['status'] = True
        respond['list'] = {inv.pk: inv.user1.username for inv in list}
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)


def accept_invite(request):
    respond = {}
    if request.user.is_authenticated and request.method == 'POST':
        data = json.loads(request.body)
        try:
            inv = FRIENDSHIP.objects.get(pk=data['pk'])
        except FRIENDSHIP.DoesNotExist:
            inv = None

        if inv is not None:
            if inv.user2 == request.user:
                inv.active = True
                inv.save()
                respond['status'] = True
                respond['mess'] = 'Invition accepted.'
            else:
                respond['status'] = False
                respond['mess'] = 'Authorisation fail.'
        else:
            respond['status'] = False
            respond['mess'] = 'Invition dosn\'t exist.'
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)

def get_my_profile(request):
    respond = {}
    if request.user.is_authenticated:
        user = usr.objects.get(pk = request.user.pk)
        lang_user = user.lang.all()
        respond['status'] = True
        respond['username'] = user.username
        respond['email'] = user.email
        respond['lang'] = {l.name: {'ISO_639_1': l.ISO_639_1, 'ISO_639_2': l.ISO_639_2} for l in lang_user}
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)


def get_users(request):
    respond = {}
    username = None
    email = None
    user = None
    if request.method == 'POST':
        if request.body is not None:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                username = data.get('username')
                email = data.get('email')
            else:
                respond['status'] = False
                respond['mess'] = 'Wrong content type.'
                return JsonResponse(respond)
    elif request.method == 'GET':
        username = request.GET.get('username')
        email = request.GET.get('email')
    else:
        respond['status'] = False
        respond['mess'] = 'Accept only post or get.'
        return JsonResponse(respond)
    try:
        if username is not None:
            if '%' in username:
                user = usr.objects.filter(username__like=username)
            else:
                user = usr.objects.get(username=username)

        if user is None and email is not None:
            if '%' in email:
                user = usr.objects.filter(email__like=email)
            else:
                user = usr.objects.filter(email=email)

    except usr.DoesNotExist:
        user = None

    if user is None and username is None and email is None:
        user = usr.objects.all()
    if user is not None:
        respond['status'] = True
        respond['mess'] = 'Operation success.'
        respond['list'] = {u.pk: {'email': u.email, 'username':  u.username} for u in user}
    else:
        respond['status'] = True
        respond['mess'] = 'User don\'t found'
    return JsonResponse(respond)
