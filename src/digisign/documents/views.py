import base64
import logging

from kitchenart.log.views import LogViewSetMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from OpenSSL import crypto
from rest_framework.views import APIView

from digisign import settings
from digisign.documents.helpers import Certificate, sanitize_signature, to_binary
from digisign.documents.models import Document
from digisign.documents.serializers import DocumentSerializer

log = logging.getLogger(__name__)


class DocumentViewSet(LogViewSetMixin):
    entity = 'document'
    queryset = Document.objects.all()
    permission_classes = [AllowAny]
    serializer_class = DocumentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    ordering_fields = ['created']

    @action(detail=True, methods=['get'], name='sign')
    def sign(self, request, id=None):
        document = Document.objects.filter(id=id).first()

        # Create object
        certificate = Certificate(settings.CERTIFICATE_PATH, settings.PASSWORD)

        # Signing Document
        file = document.document
        sign = crypto.sign(certificate.private_key, file.read(), settings.DIGEST)
        file.close()

        # Signature Result
        signature = base64.b64encode(sign)

        # Saving Document Signature
        document.signature = signature
        document.save()

        return Response({
            'signature': str(signature)
        })


class VerifyDocumentViewSet(APIView):
    def post(self, request):
        # Create object.
        certificate = Certificate(settings.CERTIFICATE_PATH, settings.PASSWORD)

        # Data.
        file = request.data.get('document').file
        sign = to_binary(request.data.get('signature'))
        result = False

        try:
            # Call crypto.verify --> (Object x509, sign, data, digest).
            crypto.verify(certificate.x509, sign, file.read(), settings.DIGEST)
            result = True
        except crypto.Error as error:
            # Log.
            log.error(
                '[ERROR][pyOpenSSL - Verify]: {error} '.format(error=str(error)))
        finally:
            file.close()

        return Response({
            'result': result
        })
