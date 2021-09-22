from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from django.conf import settings

from digisign.access_groups.views import AccessGroupViewSet
from digisign.documents.views import DocumentViewSet, VerifyDocumentViewSet
from digisign.modules.views import ModuleViewSet, StaffModuleAPIView
from digisign.users.views import StaffViewSet

router = DefaultRouter()

router.register('module', ModuleViewSet, basename='module')
router.register('access-group', AccessGroupViewSet, basename='access_group')
router.register('document', DocumentViewSet, basename='document')
router.register('staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('auth/', include('digisign.auth.urls', namespace='auth')),
    path('document/verify/', VerifyDocumentViewSet.as_view(), name='document_verify'),
    path('staff/module/', StaffModuleAPIView.as_view(), name='staff_module'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)