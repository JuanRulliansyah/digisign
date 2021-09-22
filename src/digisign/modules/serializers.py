from kitchenart.drf import TimestampedSerializerMixin
from rest_framework import serializers

from digisign.modules.models import Module


class ModuleSerializer(TimestampedSerializerMixin, serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        modules = Module.objects.filter(parent=obj.pk, is_active=True)
        return ModuleSerializer(
            modules,
            many=True,
            context={'request': self.context.get('request')}
        ).data

    class Meta:
        model = Module
        fields = (
            'href',
            'name',
            'icon',
            'is_active',
            'path',
            'parent',
            'sort_priority',
            'children'
        )
        extra_kwargs = {
            'href': {'lookup_field': 'slug', },
            'parent': {'lookup_field': 'slug', }
        }

    def create(self, validated_data):
        instance = super().create(validated_data=validated_data)
        Module.objects.update_path(instance=instance)
        return instance

    def update(self, instance, validated_data):
        Module.objects.update_path(instance=instance, save=False)
        return super().update(instance=instance, validated_data=validated_data)


class StaffModuleTreeSerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_superuser:
            modules = Module.objects.filter(parent=obj.pk, is_active=True)
        else:
            modules = user.access_group.modules.filter(parent=obj.pk, is_active=True)

        return StaffModuleTreeSerializer(
            modules,
            many=True,
            context={'request': self.context.get('request')}
        ).data

    class Meta:
        model = Module
        fields = (
            'href',
            'name',
            'icon',
            'path',
            'children'
        )
        extra_kwargs = {
            'href': {'lookup_field': 'slug', }
        }
