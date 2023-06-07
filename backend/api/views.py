import json

from django.contrib.auth import login as log, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from api.models import User as usr, LANGUAGE as lang, FRIENDSHIP, GENRE, GAME, EVENT, EVENT_PARTICIPANTS
from datetime import date, datetime


class IndexView(APIView):
    def get(self, request):
        respond = {'Mess': "This is the api."}
        if request.user.is_authenticated:
            respond['LoginStatus'] = True
        return JsonResponse(respond)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            log(request, user)
            # User credentials are valid
            return Response({'status': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # User credentials are invalid
            return Response({'status': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'Logout success.'})
        return JsonResponse({'status': 'Logout failed'})

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'Logout success.'})
        return JsonResponse({'status': 'Logout failed'})


class RegisterView(APIView):
    def post(self, request):
        respond = {}
        if request.method == 'POST':
            data = request.data
            email = data.get('email')
            username = data.get('username')
            password = data.get('password1')
            if data.get('password1') != data.get('password2'):
                respond['password'] = "Passwords are not identical."
            if usr.objects.filter(email=email).exists():
                respond['email'] = "Email is already in use."
            if usr.objects.filter(username=username).exists():
                respond['username'] = "Username is already in use."

            language = lang.get_lang(data.get('language') or 'en')

            if username == None or password == None or email == None or language == None:
                respond['field'] = 'field coulndn\'t be ampty'

            if len(respond) > 0:
                respond['mess'] = "Create new user fail"
                respond['status'] = False

                return Response(respond, status=status.HTTP_200_OK)

            if usr.objects.create_user(username=username, password=password, email=email, lang=language):
                respond['mess'] = "Create new user success"
                respond['status'] = True
            else:
                respond['mess'] = "Create new user fail"
                respond['status'] = False

            return Response(respond, status=status.HTTP_200_OK)
        else:
            respond['status'] = False
            return Response({'mess': 'Accepted only POST'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'mess': 'critical error'}, status=status.HTTP_400_BAD_REQUEST)


class IsAuthSessionView(APIView):
    def get(self, request):
        respond = {}
        if request.user.is_authenticated:
            respond['LoginStatus'] = True
            respond['username'] = request.user.username
        else:
            respond['LoginStatus'] = False
        return Response(respond, status=status.HTTP_200_OK)


class GetLangListView(APIView):
    def get(self, request):
        language = lang.objects.all()
        respond = {l.name: {'ISO_639_1': l.ISO_639_1, 'ISO_639_2': l.ISO_639_2} for l in language}
        return Response(respond, status=status.HTTP_200_OK)



class GetLangView(APIView):
    def getLang(self, name, ISO_639_1, ISO_639_2):
        language = lang.objects.filter(name=name) if name else lang.objects.filter(
            ISO_639_1=ISO_639_1) if ISO_639_1 else lang.objects.filter(
            ISO_639_2=ISO_639_2) if ISO_639_2 else lang.objects.all()
        respond = {l.name: {'ISO_639_1': l.ISO_639_1, 'ISO_639_2': l.ISO_639_2} for l in language}
        return respond
    def post(self, request):
        data = request.data
        name = data.get('name')
        ISO_639_1 = data.get('ISO_639_1')
        ISO_639_2 = data.get('ISO_639_2')
        return Response(self.getLang(name, ISO_639_1, ISO_639_2), status=status.HTTP_200_OK)
    def get(self, request):
        name = request.GET.get('name')
        ISO_639_1 = request.GET.get('ISO_639_1')
        ISO_639_2 = request.GET.get('ISO_639_2')
        return Response(self.getLang(name, ISO_639_1, ISO_639_2), status=status.HTTP_200_OK)


class UserSetDescriptionView(APIView):
    def post(self, request):
        respond = {}
        if request.user.is_authenticated:
            data = request.data
            user = usr.objects.get(pk=request.user.pk)
            user.description = data['description']
            user.save()
            respond['status'] = True
            respond['mess'] = 'User description updated.'
            respond['description'] = data['description']
        else:
            respond['status'] = False
            respond['mess'] = 'Authorisation fail.'

        return Response(respond, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    def post(self, request):
        respond = {}
        if request.user.is_authenticated:
            data = request.data
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
        return Response(respond, status=status.HTTP_200_OK if respond['status'] else status.HTTP_401_UNAUTHORIZED)


class AddFriendshipView(APIView):
    def post(self, request):
        respond = {}
        if request.user.is_authenticated:
            data = request.data
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
                return Response(respond, status=status.HTTP_200_OK if respond['status'] else status.HTTP_401_UNAUTHORIZED)
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
        return Response(respond, status=status.HTTP_200_OK if respond['status'] else status.HTTP_400_BAD_REQUEST)


class ActiveFriendshipInviteView(APIView):
    def post(self, request):
        respond = {}
        if request.user.is_authenticated:

            try:
                list = FRIENDSHIP.objects.filter(user2=request.user, active=False)
            except FRIENDSHIP.DoesNotExist:
                list = []

            respond['status'] = True
            respond['list'] = {inv.pk: inv.user1.username for inv in list}
        else:
            respond['status'] = False
            respond['mess'] = 'Authorisation fail.'
        return Response(respond, status=status.HTTP_200_OK if respond['status'] else status.HTTP_400_BAD_REQUEST)


class AcceptInviteView(APIView):
    def post(self, request):
        respond = {}
        if request.user.is_authenticated:
            data = request.data
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
        user = usr.objects.get(pk=request.user.pk)
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
        respond['list'] = {u.pk: {'email': u.email, 'username': u.username} for u in user}
    else:
        respond['status'] = True
        respond['mess'] = 'User don\'t found'
    return JsonResponse(respond)


def add_new_event(request):
    respond = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                if len(data) > 0:
                    game = data.get('game')
                    try:
                        if str(game).isdigit():
                            game = GAME.objects.get(pk=game)
                        else:
                            game = GAME.objects.get(name__like='game')
                    except GAME.DoesNotExist:
                        game = None

                    name = data.get('name')
                    creator = request.user
                    date_now = datetime.now()
                    if game is not None and name is not None:
                        event = EVENT.objects.create(name=name, game=game,
                                                     creator=usr.objects.get(pk=creator.pk), date_time=date_now)
                        respond['status'] = True
                        respond['mess'] = 'Operation success.'
                    else:
                        respond['status'] = False
                        respond['mess'] = 'Game or name don\'t exist'
                else:
                    respond['status'] = False
                    respond['mess'] = 'Body can\'t be empty'
            else:
                respond['status'] = False
                respond['mess'] = 'Content type accept only "application/json".'
        else:
            respond['status'] = False
            respond['mess'] = 'Accept ony POST.'
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)


def add_participant_to_event(request):
    respond = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                if len(data) > 0:
                    event = data.get('event')
                    try:
                        if str(event).isdigit():
                            event = EVENT.objects.get(pk=event)
                        else:
                            event = EVENT.objects.get(name__like='%{}%'.format(event))
                    except EVENT.DoesNotExist:
                        event = None
                    if not (request.user.is_staff and request.user.is_active) and event is not None:
                        if event.creator.pk != request.user.pk:
                            event_part = EVENT_PARTICIPANTS.objects.get(user=request.user)
                            if event_part is not None:
                                if not event_part.admin:
                                    respond['status'] = False
                                    respond['mess'] = 'Authorisation fail.'
                                    return JsonResponse(respond)

                    user = data.get('user')
                    try:
                        if str(user).isdigit():
                            user = usr.objects.get(pk=user)
                        else:
                            user = usr.objects.get(name__like=user)
                    except usr.DoesNotExist:
                        user = None
                    admin = data.get('admin') or False
                    if event is not None and user is not None:
                        EVENT_PARTICIPANTS.objects.create(event=event, user=user, admin=admin)
                        respond['status'] = True
                        respond['mess'] = 'Success'
                    else:
                        respond['status'] = False
                        respond['mess'] = 'Event or user does\'t exit'

                else:
                    respond['status'] = False
                    respond['mess'] = 'Body can\'t be empty'
            else:
                respond['status'] = False
                respond['mess'] = 'Content type accept only "application/json".'
        else:
            respond['status'] = False
            respond['mess'] = 'Accept ony POST.'
    else:
        respond['status'] = False
        respond['mess'] = 'Authorisation fail.'
    return JsonResponse(respond)
