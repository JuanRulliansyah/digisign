from django.shortcuts import render
from kitchenart.drf import SoftDeleteViewSetMixin
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from digisign.modules.models import Module
from digisign.modules.serializers import ModuleSerializer, StaffModuleTreeSerializer


class ModuleViewSet(SoftDeleteViewSetMixin, ModelViewSet):
    queryset = Module.objects.all()
    permission_classes = [IsAdminUser, ]
    serializer_class = ModuleSerializer
    lookup_field = 'slug'
    search_fields = ['name', 'path']
    ordering_fields = ['name', 'path', 'sort_priority']

    @action(detail=False)
    def tree(self, request):
        queryset = self.queryset.filter(parent=None, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StaffModuleAPIView(ListAPIView):
    serializer_class = StaffModuleTreeSerializer
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        user = self.request.user
        module_parent = self.request.query_params.get('parent', None)
        if user.is_superuser:
            queryset = Module.objects.filter(is_active=True)
        else:
            queryset = user.access_group.modules.filter(is_active=True)

        if module_parent:
            queryset = queryset.filter(parent__slug=module_parent)
        else:
            queryset = queryset.filter(parent=None)
        return queryset
