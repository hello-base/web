from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel


class History(TimeStampedModel):
    RESOLUTIONS = Choices('second', 'minute', 'hour', 'day', 'week', 'month', 'year')
    resolution = models.CharField(choices=RESOLUTIONS, default=RESOLUTIONS.day, max_length=6)

    tag = models.SlugField()
    datetime = models.DateTimeField()
    source_type = models.ForeignKey(ContentType)
    source_id = models.PositiveIntegerField(blank=True, null=True)
    source_object = GenericForeignKey('source_type', 'source_id')

    sum = models.IntegerField(default=0)
    delta = models.IntegerField(default=0)

    class Meta:
        get_latest_by = 'datetime'
        verbose_name_plural = 'histories'

    def __unicode__(self):
        return u'%s' % (self.tag)

    def save(self, *args, **kwargs):
        try:
            filters = {'resolution': self.resolution, 'tag': self.tag}
            previous = self._default_manager.filter(**filters).latest()
        except self._meta.model.DoesNotExist:
            pass
        else:
            self.delta = self.sum - previous.sum
        super(History, self).save(*args, **kwargs)
