import datetime
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class AbstractBaseModel(models.Model):
    # Fields
    created = models.DateTimeField(
        default=datetime.datetime.now,
        editable=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    """Пользователь"""

    # Fields
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True, null=True)
    subscribed_to_newsletters = models.BooleanField(verbose_name='Подписан на рассылки', default=True)
    telegram = models.CharField(verbose_name='Телеграм аккаунт', max_length=150, blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=50, blank=True, null=True)
    profile_photo_path = models.ImageField(verbose_name='Фото', blank=True, null=True)
    last_updated = models.DateTimeField(verbose_name='Обновлен', default=datetime.datetime.now, editable=False)
    country = models.CharField(verbose_name='Страна', max_length=150, blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=150, blank=True, null=True)
    avatar = models.ImageField(verbose_name='Аватар', blank=True, null=True)
    department = models.CharField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}. {self.username}'
