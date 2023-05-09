from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class LANGUAGE(models.Model):
    crosscut = models.CharField(max_length=30)
    name = models.CharField(max_length=100)


class USER(AbstractUser):
    description = models.CharField(max_length=1024, default="")
    lang = models.ManyToManyField(LANGUAGE)
    email = models.EmailField(_("email address"), blank=True, unique=True, null=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"
        abstract = False


class FRIENDSHIP(models.Model):
    user1 = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user2')
    create_date = models.DateField()


class GENRE(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=250, null=True)


class GAME(models.Model):
    name = models.CharField(max_length=40)
    available_lang = models.ManyToManyField(LANGUAGE)
    release_date = models.IntegerField()
    description = models.CharField(max_length=1024, null=True)
    publisher = models.CharField(max_length=50, null=True)
    genre = models.ManyToManyField(GENRE, related_name="genre")
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
