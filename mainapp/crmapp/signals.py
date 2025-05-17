from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from mainapp.settings import EMAIL_HOST_USER
from .models import Stage, Deal


@receiver(m2m_changed, sender=Stage.deals.through)
def deal_change_stage(sender, instance, **kwargs):
    """Cигнал, срабатывающий на смену поля deals при смене сделки отправляет сообщение"""
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "post_add":
        list_contacts = list(Deal.objects.filter(id__in=pk_set).values_list('contacts__email', flat=True))
        for email in list_contacts:
            send_mail(
                'Добавление в этап',
                f'Вы идобавлены в этап {instance.name}',
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
    if action == "post_remove":
        list_contacts = list(Deal.objects.filter(id__in=pk_set).values_list('contacts__email', flat=True))
        for email in list_contacts:
            send_mail(
                'Исключение из этапа',
                f'Вы исключены из этапа {instance.name}',
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
