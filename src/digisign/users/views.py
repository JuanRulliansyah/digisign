from django.contrib.auth import get_user_model
from kitchenart.drf import SoftDeleteViewSetMixin
from kitchenart.log.views import LogViewSetMixin
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from digisign.modules.models import Module
from digisign.modules.serializers import StaffModuleTreeSerializer
from digisign.users.serializers import StaffSerializer


class StaffProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class StaffViewSet(SoftDeleteViewSetMixin, LogViewSetMixin):
    entity = 'staff'
    queryset = get_user_model().objects.filter(is_staff=True)
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'email', 'date_joined']

    @action(detail=False, url_path='access-module')
    def get_access_module(self, request):
        user = self.request.user
        if user.is_superuser:
            queryset = Module.objects.filter(is_active=True)
        else:
            queryset = user.access_group.modules.filter(is_active=True)
        queryset = queryset.filter(parent=None)
        serializer = StaffModuleTreeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
