from django.db import models
from users.models import AbstractBaseModel


class Contact(AbstractBaseModel):
    """Контакт"""
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True, null=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True, null=True)
    telegram = models.CharField(verbose_name='Телеграм аккаунт', max_length=150, blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    profile_photo_path = models.ImageField(verbose_name='Фото', blank=True, null=True)
    country = models.CharField(verbose_name='Страна', max_length=150, blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=150, blank=True, null=True)
    make_delete = models.BooleanField(verbose_name='Помечен на удаление', default=False)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return str(self.id) + '. ' + self.last_name


class Deal(AbstractBaseModel):
    """Сделки"""
    name = models.CharField(verbose_name='Название сделки', max_length=150, blank=True, null=True)
    contacts = models.ManyToManyField(
        Contact,
        verbose_name='Контакты',
        blank=True,
        related_name='contacts',
        null=True,
    )

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return str(self.id) + '. ' + self.name


class Stage(AbstractBaseModel):
    """Этапы"""
    name = models.CharField(verbose_name='Название этапа', max_length=150, blank=True, null=True)
    deals = models.ManyToManyField(
        Deal,
        verbose_name='Сделки',
        related_name='deals',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = 'Этапы'

    def __str__(self):
        return str(self.id) + '. ' + self.name


class Funnel(AbstractBaseModel):
    """Воронки"""
    name = models.CharField(verbose_name='Название воронки', max_length=150, blank=True, null=True)
    stages = models.ManyToManyField(
        Stage,
        verbose_name='Этапы',
        blank=True,
        related_name='stages',
        null=True,
    )

    class Meta:
        verbose_name = 'Воронка'
        verbose_name_plural = 'Воронки'

    def __str__(self):
        return str(self.id) + '. ' + self.name
