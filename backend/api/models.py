from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime


def is_array_of_strings(value):
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return True
    else:
        return False


class LANGUAGE(models.Model):
    ISO_639_1 = models.CharField(max_length=2, unique=True)
    ISO_639_2 = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def get_lang(lang):
        if lang == None:
            return None
        elif len(lang) == 2:
            language = LANGUAGE.objects.get(ISO_639_1=lang)
        elif len(lang) == 3:
            language = LANGUAGE.objects.get(ISO_639_2=lang)
        else:
            language = LANGUAGE.objects.get(name=lang)
        return language


class UserManager(UserManager):

    def create_user(self, username, password, email, lang, description="", **extra_fields):
        if lang is None:
            return False
        if isinstance(lang, str):
            lang = LANGUAGE.get_lang(lang)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self._create_user(username, email, password, **extra_fields)
        user.lang.add(lang)
        user.description = description
        user.is_active = True
        user.save()
        return user


class User(AbstractUser):
    description = models.CharField(max_length=1024, default="")
    lang = models.ManyToManyField(LANGUAGE)
    email = models.EmailField(
        _("email address"), blank=True, unique=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"
        abstract = False


class FRIENDSHIP(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user2')
    create_date = models.DateField()
    active = models.BooleanField(default=False)


class GENRE(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=250, null=True)


class GAME(models.Model):
    name = models.CharField(max_length=40)
    available_lang = models.ManyToManyField(LANGUAGE)
    release_date = models.DateField()
    description = models.CharField(max_length=1024, null=True)
    publisher = models.CharField(max_length=50, null=True)
    genre = models.ManyToManyField(GENRE, related_name="genre")
    max_player = models.IntegerField(default=1)
    online = models.BooleanField(default=False)
    verify = models.BooleanField(default=False)

    def create_new_game(name, release_date, publisher, max_player=1, online=False, description="", available_lang=[],
                        gentres=[], date_format="DD-MM-YYYY"):
        # Data validation
        if len(available_lang) > 0:
            if not is_array_of_strings(available_lang):
                return False
        if len(gentres) > 0:
            if not is_array_of_strings(gentres):
                return False
        if isinstance(name, str) and isinstance(publisher, str) and isinstance(max_player, int) \
                and isinstance(online, bool) and isinstance(description, str) and isinstance(available_lang,
                                                                                             list) and isinstance(
            gentres, list):
            return False
        if isinstance(release_date, str):
            release_date = date.fromisoformat(release_date)
        if isinstance(release_date, int):
            release_date = datetime.strptime(release_date, date_format).date()
        # Create new game
        release_date = ("{}-{}-{}".format(release_date.year,
                                          release_date.month, release_date.day))
        game = GAME.objects.create()
        game.name = name
        game.release_date = release_date
        game.description = description
        game.publisher = publisher
        game.max_player = max_player
        for lang in available_lang:
            game.available_lang.add(LANGUAGE.objects.get(lang))
        for gentre in gentres:
            game.genre.add(GENRE.objects.get(gentre))
        game.save()


class OPINION(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    star = models.DecimalField(max_digits=2, decimal_places=1)


class EVENT(models.Model):
    name = models.CharField(max_length=256)
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()


class EVENT_PARTICIPANTS(models.Model):
    event = models.ForeignKey(EVENT, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.BooleanField()
