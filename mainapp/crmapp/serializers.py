from rest_framework import serializers
from .models import Contact, Deal, Stage, Funnel
from django.core.validators import MaxValueValidator, MinValueValidator


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализация модели контакты
    """

    class Meta:
        model = Contact
        fields = '__all__'


class ContactEditSerializer(serializers.ModelSerializer):
    """
    Сериализация модели контактов для создания и редактирования
    """

    class Meta:
        model = Contact
        fields = ('first_name', 'middle_name', 'last_name', 'phone', 'telegram', 'email',
                  'profile_photo_path', 'country', 'city',)


class DealSerializer(serializers.ModelSerializer):
    """
    Сериализация модели сделки
    """
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = Deal
        fields = ('id', 'name', 'contacts',)


class DealEditSerializer(serializers.ModelSerializer):
    """
    Сериализация модели сделка для создания и редактирования
    """

    class Meta:
        model = Deal
        fields = ('name', 'contacts',)


class DealForStageSerializer(serializers.ModelSerializer):
    """
    Сериализация модели сделки для этапов
    """

    class Meta:
        model = Deal
        fields = ('id', 'name',)


class DealEditAndAddContactSerializer(serializers.ModelSerializer):
    """
    Сериализация модели сделки для редактирования и добавления контактов
    """

    class Meta:
        model = Deal
        fields = ('name', 'contacts',)

    def validate(self, data):
        data['contacts'] += Deal.objects.filter(id=self.instance.id).values_list('contacts', flat=True)
        return data


class StageSerializer(serializers.ModelSerializer):
    """
    Сериализация модели этапов
    """
    deals = DealForStageSerializer(read_only=True, many=True)

    class Meta:
        model = Stage
        fields = ('id', 'name', 'deals',)


class StageEditSerializer(serializers.ModelSerializer):
    """
    Сериализация модели этапы для создания и редактирования
    """

    class Meta:
        model = Stage
        fields = ('name', 'deals',)


class StageEditAndAddDealSerializer(serializers.ModelSerializer):
    """
    Сериализация модели этапы для редактирования и добавления сделок
    """

    class Meta:
        model = Stage
        fields = ('name', 'deals',)

    def validate(self, data):
        data['deals'] += Stage.objects.filter(id=self.instance.id).values_list('deals', flat=True)
        return data


class StageForFunnelSerializer(serializers.ModelSerializer):
    """
    Сериализация модели этапы для воронок
    """

    class Meta:
        model = Stage
        fields = ('id', 'name',)


class FunnelSerializer(serializers.ModelSerializer):
    """
    Сериализация модели воронки
    """
    stages = StageForFunnelSerializer(read_only=True, many=True)

    class Meta:
        model = Funnel
        fields = ('id', 'name', 'stages',)


class FunnelEditSerializer(serializers.ModelSerializer):
    """
    Сериализация модели воронки для создания и редактирования
    """

    class Meta:
        model = Funnel
        fields = ('name', 'stages',)


class FunnelEditAndAddStageSerializer(serializers.ModelSerializer):
    """
    Сериализация модели воронки для редактирования и добавление этапов
    """

    class Meta:
        model = Funnel
        fields = ('name', 'stages',)

    def validate(self, data):
        data['stages'] += Funnel.objects.filter(id=self.instance.id).values_list('stages', flat=True)
        return data


class RequestChangeDealSerializer(serializers.ModelSerializer):
    """
    Сериализатор запроса на перермещение сделки с одного этапа в другой
    """
    stage_id_out = serializers.PrimaryKeyRelatedField(source='id', queryset=Stage.objects.all())
    stage_id_in = serializers.IntegerField(validators=[MinValueValidator(1)])
    deal_id = serializers.PrimaryKeyRelatedField(source='deals', queryset=Deal.objects.all())

    class Meta:
        model = Stage
        fields = ('stage_id_out', 'stage_id_in', 'deal_id')

    def validate(self, data):
        if data['stage_id_in'] not in Stage.objects.all().values_list('id', flat=True):
            raise serializers.ValidationError('Укажите корректный id этапа.')
        old_stage = Stage.objects.filter(id=data['id'].id, deals__id=data['deals'].id)
        if not old_stage:
            raise serializers.ValidationError('У этапа нет такой сделки')
        return data


class RequestChangeDealToFunnelSerializer(serializers.ModelSerializer):
    """
    Сериализатор запроса на перермещение сделки с одного этапа в другой
    """
    stage_id_out = serializers.PrimaryKeyRelatedField(source='steges', queryset=Stage.objects.all())
    stage_id_in = serializers.IntegerField(validators=[MinValueValidator(1)])
    deal_id = serializers.IntegerField(validators=[MinValueValidator(1)])
    funnel_id_out = serializers.PrimaryKeyRelatedField(source='id', queryset=Funnel.objects.all())
    funnel_id_in = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Funnel
        fields = ('stage_id_out', 'stage_id_in', 'deal_id', 'funnel_id_out', 'funnel_id_in')

    def validate(self, data):
        if data['stage_id_in'] not in Stage.objects.all().values_list('id', flat=True):
            raise serializers.ValidationError('Укажите корректный id этапа.')
        if data['deal_id'] not in Deal.objects.all().values_list('id', flat=True):
            raise serializers.ValidationError('Укажите корректный id сделки.')
        if data['funnel_id_in'] not in Funnel.objects.all().values_list('id', flat=True):
            raise serializers.ValidationError('Укажите корректный id воронки.')
        old_stage = Stage.objects.filter(id=data['steges'].id, deals__id=data['deal_id'])
        if not old_stage:
            raise serializers.ValidationError('У этапа нет такой сделки')
        old_funnel = Funnel.objects.filter(id=data['id'].id, stages__id=data['steges'].id)
        if not old_funnel:
            raise serializers.ValidationError('У воронки отдающей нет такого этапа')
        new_funnel = Funnel.objects.filter(id=data['funnel_id_in'], stages__id=data['stage_id_in'])
        if not new_funnel:
            raise serializers.ValidationError('У воронки принимающей нет такого этапа')

        return data


class FunnelForChangeDealSerializer(serializers.ModelSerializer):
    """
    Сериализация модели воронки
    """
    stages = StageSerializer(read_only=True, many=True)

    class Meta:
        model = Funnel
        fields = ('id', 'name', 'stages',)
