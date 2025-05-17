from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginAPIView, TokenRefreshView

router = DefaultRouter()

router.register('user', UserViewSet, basename="users-view")

urlpatterns = router.urls

urlpatterns += [
    path('auth/', LoginAPIView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
