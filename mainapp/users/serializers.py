from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    """
    Валидация данных при авторизации
    """
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(max_length=200, allow_blank=False)


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация модели пользователя
    """
    user_role = serializers.SerializerMethodField('get_user_role')
    updated_at = serializers.DateTimeField(source='last_updated')
    created_at = serializers.DateTimeField(source='date_joined')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'middle_name', 'last_name', 'avatar', 'city', 'country',
                  'phone', 'telegram', 'email', 'user_role',
                  'last_login', 'created_at', 'updated_at', 'department', 'subscribed_to_newsletters')

    def get_user_role(self, obj):
        return obj.groups.first().name if obj.groups.exists() else None


class ResponseLoginSerializer(serializers.ModelSerializer):
    """
    Сериализатор ответа после успешной авторизации
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    role = serializers.CharField(source='groups.name')

    class Meta:
        model = User
        fields = ('access', 'refresh', 'role', 'first_name', 'last_name')


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализация модели пользователя для list
    """
    group_id = serializers.SerializerMethodField('get_group_id')
    updated_at = serializers.DateTimeField(source='last_updated')
    created_at = serializers.DateTimeField(source='date_joined')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'phone', 'telegram', 'email',
                  'group_id', 'last_login', 'created_at', 'updated_at', )

    def get_group_id(self, obj):
        return obj.groups.first().id if obj.groups.exists() else None


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализация модели пользователя для одной записи
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'avatar', 'city', 'country',
                  'phone', 'telegram', 'email', 'department', 'subscribed_to_newsletters')


class RequestUserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализация модели пользователя для редактирования
    """

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'phone', 'telegram', 'email', )
