from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import generics, mixins

from .serializers import ContactSerializer, ContactEditSerializer, DealSerializer, DealEditSerializer, \
    StageSerializer, StageEditSerializer, FunnelSerializer, FunnelEditSerializer, RequestChangeDealSerializer, \
    RequestChangeDealToFunnelSerializer, FunnelForChangeDealSerializer, FunnelEditAndAddStageSerializer, \
    StageEditAndAddDealSerializer, DealEditAndAddContactSerializer

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.paginators import UserListPaginator

from .models import Contact, Deal, Stage, Funnel


@extend_schema(tags=['CRUD Контакты'], )
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех контактов",
        responses=ContactSerializer
    ),
    retrieve=extend_schema(
        summary="Получение информации по конкретному контакту",
        responses=ContactSerializer
    ),
    create=extend_schema(
        request=ContactEditSerializer,
        summary="Создание контакта",
        responses=ContactSerializer
    ),
    update=extend_schema(
        request=ContactEditSerializer,
        summary="Изменение существующего контакта",
        responses=ContactSerializer
    ),
    partial_update=extend_schema(
        request=ContactEditSerializer,
        summary="Частичное изменение данных о контакта",
        responses=ContactSerializer
    ),
    destroy=extend_schema(
        summary="Удаление контакта",
    ),

)
class ContactViewSet(viewsets.ModelViewSet):
    """
    API CRUD для контактов с фильтроми
    """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = UserListPaginator
    search_fields = ['first_name__icontains', 'middle_name__icontains',
                     'last_name__icontains', 'phone__contains', 'telegram__icontains', 'email__icontains']

    def get_queryset(self):
        return Contact.objects.filter(make_delete=False)

    def get_serializer_class(self):
        if self.action == 'list':
            return ContactSerializer
        if self.action == 'retrieve':
            return ContactSerializer
        if self.action == 'update':
            return ContactEditSerializer
        if self.action == 'partial_update':
            return ContactEditSerializer
        if self.action == 'create':
            return ContactEditSerializer

    def perform_destroy(self, instance):
        del_contact = Contact.objects.get(id=instance.id)
        if del_contact:
            del_contact.make_delete = True
            del_contact.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_contact = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(ContactSerializer(new_contact).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(ContactSerializer(instance).data)


@extend_schema(tags=['CRUD сделка'], )
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех сделок",
        responses=DealSerializer
    ),
    retrieve=extend_schema(
        summary="Получение информации по конкретной сделки",
        responses=DealSerializer
    ),
    create=extend_schema(
        request=DealEditSerializer,
        summary="Создание сделки",
        responses=DealSerializer
    ),
    update=extend_schema(
        request=DealEditSerializer,
        summary="Изменение существующей сделки",
        responses=DealSerializer
    ),
    partial_update=extend_schema(
        request=DealEditAndAddContactSerializer,
        summary="Изменение названия сделки и добавление контактов",
        responses=DealSerializer
    ),
    destroy=extend_schema(
        summary="Удаление сделки",
    ),

)
class DealViewSet(viewsets.ModelViewSet):
    """
    API CRUD для сделки с фильтроми
    """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = UserListPaginator
    search_fields = ['name__icontains']

    def get_queryset(self):
        return Deal.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return DealSerializer
        if self.action == 'retrieve':
            return DealSerializer
        if self.action == 'update':
            return DealEditSerializer
        if self.action == 'partial_update':
            return DealEditAndAddContactSerializer
        if self.action == 'create':
            return DealEditSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_deal = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(DealSerializer(new_deal).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(DealSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(DealSerializer(instance).data)


@extend_schema(tags=['CRUD этапов'], )
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех этапов",
        responses=StageSerializer
    ),
    retrieve=extend_schema(
        summary="Получение информации по конкретному этапу",
        responses=StageSerializer
    ),
    create=extend_schema(
        request=StageEditSerializer,
        summary="Создание этапа",
        responses=StageSerializer
    ),
    update=extend_schema(
        request=StageEditSerializer,
        summary="Изменение существующего этапа",
        responses=StageSerializer
    ),
    partial_update=extend_schema(
        request=StageEditAndAddDealSerializer,
        summary="Изменение названия этапа и добавление сделок",
        responses=StageSerializer
    ),
    destroy=extend_schema(
        summary="Удаление этапа",
    ),

)
class StageViewSet(viewsets.ModelViewSet):
    """
    API CRUD для этапов с фильтроми
    """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = UserListPaginator
    search_fields = ['name__icontains']

    def get_queryset(self):
        return Stage.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StageSerializer
        if self.action == 'retrieve':
            return StageSerializer
        if self.action == 'update':
            return StageEditSerializer
        if self.action == 'partial_update':
            return StageEditAndAddDealSerializer
        if self.action == 'create':
            return StageEditSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_stage = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(StageSerializer(new_stage).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(StageSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(StageSerializer(instance).data)


@extend_schema(tags=['CRUD воронок'], )
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех воронок",
        responses=FunnelSerializer
    ),
    retrieve=extend_schema(
        summary="Получение информации по конкретной воронке",
        responses=FunnelSerializer
    ),
    create=extend_schema(
        request=FunnelEditSerializer,
        summary="Создание воронки",
        responses=FunnelSerializer
    ),
    update=extend_schema(
        request=FunnelEditSerializer,
        summary="Изменение существующей воронки (изменение этапов воронки)",
        responses=FunnelSerializer
    ),
    partial_update=extend_schema(
        request=FunnelEditAndAddStageSerializer,
        summary="Изменение названия воронки и добавление этапов воронки",
        responses=FunnelSerializer
    ),
    destroy=extend_schema(
        summary="Удаление воронки",
    ),

)
class FunnelViewSet(viewsets.ModelViewSet):
    """
    API CRUD для воронки с фильтроми
    """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = UserListPaginator
    search_fields = ['name__icontains']

    def get_queryset(self):
        return Funnel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return FunnelSerializer
        if self.action == 'retrieve':
            return FunnelSerializer
        if self.action == 'update':
            return FunnelEditSerializer
        if self.action == 'partial_update':
            return FunnelEditAndAddStageSerializer
        if self.action == 'create':
            return FunnelEditSerializer
        if self.action == 'change_deal_in_funnel_to_funnel':
            return RequestChangeDealToFunnelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_funnel = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(FunnelSerializer(new_funnel).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(FunnelSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(FunnelSerializer(instance).data)

    @extend_schema(
        summary="Перенос сделки из одной воронки в другую",
        request=RequestChangeDealToFunnelSerializer,
        responses=FunnelForChangeDealSerializer
    )
    @action(detail=False, methods=['PATCH'], description="Перенос сделки из одной воронки в другую",
            url_path='deal_change_funnel',
            url_name='deal_change_funnel', serializer_class=RequestChangeDealToFunnelSerializer)
    def change_deal_in_funnel_to_funnel(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_stage = Stage.objects.get(id=serializer.data['stage_id_in'])
        old_stage = Stage.objects.get(id=serializer.data['stage_id_out'], deals__id=serializer.data['deal_id'])
        old_stage.deals.remove(Deal.objects.get(id=serializer.data['deal_id']))
        old_stage.save()
        new_stage.deals.add(Deal.objects.get(id=serializer.data['deal_id']))
        new_stage.save()
        new_funnel = Funnel.objects.get(id=serializer.data['funnel_id_in'])
        return Response(FunnelForChangeDealSerializer(new_funnel).data)


@extend_schema(tags=['Изменение сделки из этапа в этап'], )
@extend_schema_view(
    update=extend_schema(
        request=RequestChangeDealSerializer,
        summary="Изменение сделки из этапа в этап",
        responses=StageSerializer
    ),
)
class ChangeDealInStageView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
        API Изменение сделки из этапа в этап
        """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = RequestChangeDealSerializer
    queryset = Stage.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_stage = Stage.objects.get(id=serializer.data['stage_id_in'])
        old_stage = Stage.objects.get(id=serializer.data['stage_id_out'])
        old_stage.deals.remove(Deal.objects.get(id=serializer.data['deal_id']))
        old_stage.save()
        new_stage.deals.add(Deal.objects.get(id=serializer.data['deal_id']))
        new_stage.save()
        return Response(StageSerializer(new_stage).data)
