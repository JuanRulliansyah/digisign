from django.db import models
from gramedia.django.abstract_models import TimestampedModel
from upload_validator import FileTypeValidator

from digisign.users.models import User


class Document(TimestampedModel):
    user = models.ForeignKey(
        User,
        related_name='documents',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    document = models.FileField(
        'user document file',
        upload_to='user/document',
        blank=True,
        null=True
    )
    signature = models.TextField(blank=True)

    class Meta:
        db_table = 'document'
        ordering = ('created',)
