from collections import deque

from django.db import models
from gramedia.django.abstract_models import ManuallySortedModel
from kitchenart.models import BaseModel


class ModuleManager(models.Manager):
    def update_path(self, instance=None, save=True) -> None:
        to_update = [instance, ] if instance else self.all()
        for module in to_update:
            module.depth = len(module.ancestors) + 1
            module.path = '/'.join([mod.slug for mod in module.ancestors] + [module.slug])
            if save:
                module.save()


class Module(ManuallySortedModel, BaseModel):
    icon = models.CharField('icon', max_length=50, blank=True)
    depth = models.PositiveSmallIntegerField(default=1)
    path = models.CharField(blank=True, max_length=255)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='parent module'
    )

    objects = ModuleManager()

    class Meta:
        db_table = 'auth_module'
        ordering = ('sort_priority',)

    @property
    def ancestors(self):
        """ Returns a list of ancestors.  Root ancestor will be at position 0 (left-most),
        and the right-most element will be the most recent ancestor (direct parent)
        """
        ancestors = deque()
        module = self
        while module.parent:
            module = module.parent
            ancestors.appendleft(module)
        return ancestors
