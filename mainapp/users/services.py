from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


def check_data_for_login(data):
    """
    Проверка данных при автоизации на то, что
    - пользователь существует
    - учетная запись активирована
    - авторизационные данные совпадают
    При успешной проверки формируются ключи JWT
    :param data: Отправленные при авторизации параметры
    :return: Данные для ответа и статус ответа
    """
    username = data.get('username', None)
    password = data.get('password', None)

    if not User.objects.filter(username__iexact=username.strip()).exists():
        return {
                   'error': 'Такого пользователя не существует'}, status.HTTP_401_UNAUTHORIZED

    user = User.objects.get(username__iexact=username.strip())

    if user.is_active is False:
        return {
                   'error': 'Учетная запись не активна'}, status.HTTP_401_UNAUTHORIZED

    user = authenticate(username=user.username, password=password)

    if user is None:
        return {'error': 'Неправильный пароль'}, status.HTTP_401_UNAUTHORIZED

    refresh = RefreshToken.for_user(user)

    refresh.payload.update({
        'user_id': user.id,
        'username': user.username
    })
    update_last_login(None, user)
    return {
               'access': str(refresh.access_token),
               'refresh': str(refresh),
               'role': user.groups.values_list('name', flat=True)[0] if len(
                   user.groups.values_list('name', flat=True)) else None,
               'first_name': user.first_name if user.first_name else None,
               'last_name': user.last_name if user.last_name else None,
           }, status.HTTP_200_OK
