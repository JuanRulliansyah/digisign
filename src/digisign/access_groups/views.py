from django.shortcuts import render
from kitchenart.drf import SoftDeleteViewSetMixin
from kitchenart.log.views import LogViewSetMixin
from rest_framework.permissions import IsAdminUser

from digisign.access_groups.models import AccessGroup
from digisign.access_groups.serializers import AccessGroupSerializer


class AccessGroupViewSet(SoftDeleteViewSetMixin, LogViewSetMixin):
    entity = 'access_group'
    queryset = AccessGroup.objects.all()
    permission_classes = [IsAdminUser, ]
    serializer_class = AccessGroupSerializer
    lookup_field = 'slug'
    search_fields = ['name', ]
    ordering_fields = ['name', ]
