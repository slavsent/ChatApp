from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import LoginSerializer, ResponseLoginSerializer, UserSerializer, UserListSerializer, \
    UserCreateSerializer, RequestUserUpdateSerializer

from .services import check_data_for_login

from rest_framework_simplejwt.views import TokenRefreshView as UrbanTokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import User
from .paginators import UserListPaginator


@extend_schema(summary='Авторизация', request=LoginSerializer, responses=ResponseLoginSerializer)
class LoginAPIView(APIView):
    """
    API авторизации
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data_answer, status_answer = check_data_for_login(serializer.validated_data)

        return Response(data_answer, status=status_answer)


@extend_schema(tags=['CRUD Пользователя'], )
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех пользователей",
        responses=UserListSerializer
    ),
    retrieve=extend_schema(
        summary="Получение информации по конкретному пользователю",
        responses=UserSerializer
    ),
    create=extend_schema(
        request=UserCreateSerializer,
        summary="Создание пользователя",
        responses=UserCreateSerializer
    ),
    update=extend_schema(
        request=RequestUserUpdateSerializer,
        summary="Изменение существующего пользователя",
        responses=RequestUserUpdateSerializer
    ),
    partial_update=extend_schema(
        request=RequestUserUpdateSerializer,
        summary="Частичное изменение данных о пользователе",
        responses=RequestUserUpdateSerializer
    ),
    destroy=extend_schema(
        summary="Удаление пользователя",
    ),

)
class UserViewSet(viewsets.ModelViewSet):
    """
    API CRUD для пользователей с фильтром по группам и ролям
    """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = UserListPaginator
    search_fields = ['username__icontains', 'first_name__icontains', 'middle_name__icontains',
                     'last_name__icontains', 'phone__contains', 'telegram__icontains', 'email__icontains']

    def get_queryset(self):
        if not self.request.user.groups.name == 'admin"':
            return User.objects.filter(id=self.request.user.id, is_active=True)
        else:
            return User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'retrieve':
            return UserSerializer
        if self.action == 'update':
            return RequestUserUpdateSerializer
        if self.action == 'partial_update':
            return RequestUserUpdateSerializer
        if self.action == 'create':
            return UserCreateSerializer


@extend_schema(summary='Refresh access token', )
class TokenRefreshView(UrbanTokenRefreshView):
    """
    Переопределения для swagger класса refresh token
    """
    serializer_class = TokenRefreshSerializer
