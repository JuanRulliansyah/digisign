from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from digisign.documents.models import Document
from digisign.utils.validators import DocumentBase64File


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    document = DocumentBase64File(required=True)

    class Meta:
        model = Document
        fields = (
            'href',
            'document',
            'signature',
        )
        extra_kwargs = {
            'href': {
                'lookup_field': 'id',
                'view_name': 'document-detail'
            }
        }

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        document = super().create(validated_data=validated_data)
        return document


