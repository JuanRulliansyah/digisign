from kitchenart.drf import TimestampedSerializerMixin, get_entity_href_serializer
from kitchenart.helpers import ParseIdentityHyperlink
from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField

from digisign.access_groups.models import AccessGroup
from digisign.modules.models import Module


class AccessGroupSerializer(TimestampedSerializerMixin, HyperlinkedModelSerializer):
    user_count = SerializerMethodField()
    modules = get_entity_href_serializer(model_class=Module, many=True)

    def get_user_count(self, obj: AccessGroup):
        return obj.users.filter(is_active=True).count()

    class Meta:
        model = AccessGroup
        fields = (
            'href',
            'name',
            'user_count',
            'is_active',
            'is_deleted',
            'modules',
        )
        extra_kwargs = {
            'href': {
                'lookup_field': 'slug',
                'view_name': 'access_group-detail',
            },
            'modules': {'lookup_field': 'slug'},
        }

    def create(self, validated_data):
        validated_data.pop('modules')
        group = super().create(validated_data=validated_data)
        self.add_module_to_group(group)
        return group

    def update(self, instance, validated_data):
        if validated_data.get('modules') is not None:
            validated_data.pop('modules')

        group = super().update(instance=instance, validated_data=validated_data)
        if self.initial_data.get('modules'):
            group.modules.clear()
            self.add_module_to_group(group)
        return group

    def add_module_to_group(self, group: AccessGroup):
        module_identities = ParseIdentityHyperlink('slug', self.initial_data['modules'])
        for module_slug in module_identities.get_entity_list_identity():
            module = Module.objects.get(slug=module_slug)
            group.modules.add(module)
