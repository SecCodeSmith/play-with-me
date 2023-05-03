from django.contrib.auth.models import AbstractUser
from django.db import models


class TAG(models.Model):
    tag_name = models.CharField(max_length=40)
    types = models.CharField(max_length=1)


class LANGUAGE(models.Model):
    name = models.CharField(max_length=30)


class COUNTRY(models.Model):
    name = models.CharField(max_length=30)
    lang = models.ForeignKey(LANGUAGE, on_delete=models.CASCADE)


class USER(AbstractUser):
    description = models.CharField(max_length=1024, default="")
    lang = models.ForeignKey(LANGUAGE, on_delete=models.CASCADE, default=1)


class TAGS_USER(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    tags = models.ForeignKey(TAG, on_delete=models.CASCADE)
    tags = models.ForeignKey(TAG, on_delete=models.CASCADE)


class FRIENDSHIP(models.Model):
    user1 = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user2')
    create_date = models.DateField()


class GENRE(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=250)


class COMPANY(models.Model):
    date_of_incorporation = models.DateField()
    name = models.CharField(max_length=30)
    country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)


class GAME(models.Model):
    name = models.CharField(max_length=40)
    available_lang = models.ForeignKey(LANGUAGE, on_delete=models.CASCADE)
    release_date = models.DateField()
    description = models.CharField(max_length=1024)
    developer = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, related_name='developer')
    publisher = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, related_name='publisher')


class TAGS_GAME(models.Model):
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    tags = models.ForeignKey(TAG, on_delete=models.CASCADE)


class GAME_GENRE(models.Model):
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    genre = models.ForeignKey(GENRE, on_delete=models.CASCADE)


class OPINION(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    star = models.DecimalField(max_digits=2, decimal_places=1)


class EVENT(models.Model):
    game = models.ForeignKey(GAME, on_delete=models.CASCADE)
    users = models.ForeignKey(USER, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
