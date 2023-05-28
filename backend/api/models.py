from django.contrib.auth.models import AbstractUser
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
    ISO_639_1 = models.CharField(max_length=2)
    ISO_639_2 = models.CharField(max_length=3)
    name = models.CharField(max_length=100)


class USER(AbstractUser):
    description = models.CharField(max_length=1024, default="")
    lang = models.ManyToManyField(LANGUAGE)
    email = models.EmailField(
        _("email address"), blank=True, unique=True, null=True)

    def create_user(username, password, email, lang, description=""):
        #lang = LANGUAGE.objects.get(lang)
        #if lang is None:
        #    return False

        user = USER.objects.create_user(username=username, password=password)
        #user.lang.add(lang)
        user.email = email
        user.description = description
        user.is_active = True
        user.save()
        return True

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"
        abstract = False


class FRIENDSHIP(models.Model):
    user1 = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='user2')
    create_date = models.DateField()


class GENRE(models.Model):
    name = models.CharField(max_length=40)
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

    def create_new_game(name, release_date, publisher, max_player=1, online=False, description="", available_lang=[], gentres=[], date_format="DD-MM-YYYY"):
        # Data validation
        if len(available_lang) > 0:
            if not is_array_of_strings(available_lang):
                return False
        if len(gentres) > 0:
            if not is_array_of_strings(gentres):
                return False
        if isinstance(name, str) and isinstance(publisher, str) and isinstance(max_player, int) \
                and isinstance(online, bool) and isinstance(description, str) and isinstance(available_lang, list) and isinstance(gentres, list):
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
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    star = models.DecimalField(max_digits=2, decimal_places=1)


class EVENT(models.Model):
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    creator = models.ForeignKey(USER, on_delete=models.CASCADE)
    date_time = models.DateTimeField()


class EVENT_PARTICIPANTS(models.Model):
    event = models.ForeignKey(EVENT, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    modelator = models.BooleanField()
    admin = models.BooleanField()
