from django.contrib.auth.models import AbstractUser
from django.db import models


class LANGUAGE(models.Model):
    crosscut = models.CharField(max_length=30)
    name = models.CharField(max_length=100)


class COUNTRY(models.Model):
    name = models.CharField(max_length=30)
    lang = models.ForeignKey(LANGUAGE, on_delete=models.CASCADE)


class USER(AbstractUser):
    description = models.CharField(max_length=1024, default="")
    lang = models.ForeignKey(LANGUAGE, on_delete=models.CASCADE, default=1)


class FRIENDSHIP(models.Model):
    user1 = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user2')
    create_date = models.DateField()


class GENRE(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=250, null=True)


class GAME(models.Model):
    name = models.CharField(max_length=40)
    available_lang = models.ForeignKey(LANGUAGE, on_delete=models.CASCADE, null=True)
    release_date = models.IntegerField()
    description = models.CharField(max_length=1024, null=True)
    publisher = models.CharField(max_length=50, null=True)
    genre = models.ManyToManyField(GENRE, null=True, related_name="genre")
    max_player = models.IntegerField(default=1)
    online = models.BooleanField(default=False)


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
