from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel


class History(TimeStampedModel):
    RESOLUTIONS = Choices('second', 'minute', 'hour', 'day', 'week', 'month', 'year')
    resolution = models.CharField(choices=RESOLUTIONS, default=RESOLUTIONS.day, max_length=6)

    tag = models.SlugField()
    source_type = models.ForeignKey(ContentType)
    source_id = models.PositiveIntegerField(blank=True, null=True)

    sum = models.IntegerField(default=0)
    delta = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'histories'

    def __unicode__(self):
        return u'%s' % (self.tag)
