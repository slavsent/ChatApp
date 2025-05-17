from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ContactViewSet, DealViewSet, StageViewSet, FunnelViewSet, ChangeDealInStageView

router = DefaultRouter()
router.register('contacts', ContactViewSet, basename="contacts-view")
router.register('deals', DealViewSet, basename="deals-view")
router.register('stages', StageViewSet, basename="stages-view")
router.register('funnels', FunnelViewSet, basename="funnels-view")

urlpatterns = router.urls

urlpatterns += [
    path('deal_change_stage', ChangeDealInStageView.as_view(), name='deal-change-stage'),
]
