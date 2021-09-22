from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from kitchenart.drf import get_entity_href_serializer
from kitchenart.helpers import ParseIdentityHyperlink
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.serializers import HyperlinkedModelSerializer

from digisign.access_groups.models import AccessGroup


class StaffSerializer(HyperlinkedModelSerializer):
    first_name = serializers.CharField(label='first name', required=True)
    access_group = get_entity_href_serializer(
        model_class=AccessGroup,
        meta_extra_kwargs={
            'href': {
                'lookup_field': 'slug',
                'view_name': 'access_group-detail',
            }
        }
    )

    class Meta:
        model = get_user_model()
        fields = (
            'href',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'date_joined',
            'access_group',
            'is_active',
            'is_deleted',
        )
        extra_kwargs = {
            'href': {
                'lookup_field': 'username',
                'view_name': 'staff-detail'
            },
        }

    def create(self, validated_data):
        parse_href = ParseIdentityHyperlink('slug')
        access_group_href = self.initial_data.get('access_group').get('href')
        access_group_slug = parse_href.parse_identity_from_href(href=access_group_href)

        try:
            validated_data['access_group'] = AccessGroup.objects.get(slug=access_group_slug)
        except AccessGroup.DoesNotExist:
            raise NotFound(_('Access Group is not exists'))

        validated_data['is_staff'] = True
        staff = super().create(validated_data=validated_data)

        password = get_user_model().objects.make_random_password(length=8)
        staff.set_password('password')
        staff.save(update_fields=['password'])

        return staff

    def update(self, instance, validated_data):
        access_group = self.initial_data.get('access_group')
        if access_group:
            parse_href = ParseIdentityHyperlink('slug')
            access_group_href = access_group.get('href')
            access_group_slug = parse_href.parse_identity_from_href(href=access_group_href)
            try:
                validated_data['access_group'] = AccessGroup.objects.get(slug=access_group_slug)
            except AccessGroup.DoesNotExist:
                raise NotFound('Access Group is not exists')

        return super().update(instance=instance, validated_data=validated_data)
