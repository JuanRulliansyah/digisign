from django.db import models
from kitchenart.models import BaseModel

from digisign.modules.models import Module


class AccessGroup(BaseModel):
    modules = models.ManyToManyField(
        Module,
        verbose_name='modules',
        blank=True,
        related_name='access_groups'
    )

    class Meta:
        db_table = 'access_group'
        ordering = ('name', )
