# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from model_utils import Choices

from components.events.models import Event
from components.people.models import Group, Idol
from components.merchandise.music.models import Album, Single

User = get_user_model()


class Item(models.Model):
    CATEGORIES = Choices(
        ('announcement', 'Announcement'),
        ('appearance', 'Appearance'),
        ('audition', 'Audition'),
        ('event', 'Event'),
        ('goods', 'Goods'),
        ('graduation', 'Graduation'),
        ('musicvideo', 'Preview'),
        ('release', 'Release'),
        ('rumor', 'Rumor'),
        ('other', 'Other'),
    )
    CLASSIFICATION = Choices(
        ('major', 'Major'),
        ('important', 'Important'),
        ('normal', 'Normal'),
        ('minor', 'Minor'),
    )

    category = models.CharField(choices=CATEGORIES, max_length=16)
    classification = models.CharField(choices=CLASSIFICATION, default=CLASSIFICATION.normal, max_length=16)
    title = models.CharField(max_length=500)
    published = models.DateField(default=date.today())
    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_submissions')
    body = models.TextField(blank=True)
    slug = models.SlugField(max_length=200)

    # Involvement.
    idols = models.ManyToManyField(Idol, blank=True, null=True, related_name='%(class)ss')
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='%(class)ss')
    singles = models.ManyToManyField(Single, blank=True, null=True, related_name='%(class)ss')
    albums = models.ManyToManyField(Album, blank=True, null=True, related_name='%(class)ss')
    events = models.ManyToManyField(Event, blank=True, null=True, related_name='%(class)ss')

    # Sources.
    source = models.CharField(blank=True, max_length=200,
        help_text='Separate multiple sources by comma (must have accompanying URL).')
    source_url = models.URLField('source URL', blank=True,
        help_text='Seperate multile URLs with comma (must have accompanying Source).')
    via = models.CharField(blank=True, max_length=200)
    via_url = models.URLField('via URL', blank=True)

    class Meta:
        ordering = ('-published',)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.published)


class ItemImage(models.Model):
    parent = models.ForeignKey(Item, related_name='images')

    image = models.ImageField(blank=True, upload_to='news/')
    caption = models.CharField(blank=True, max_length=500)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})

    def __unicode__(self):
        return '%s' % (self.image)


class Update(models.Model):
    parent = models.ForeignKey(Item, related_name='updates')
    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_submissions')
    published = models.DateField(default=date.today())
    body = models.TextField(blank=True)

    # Sources.
    source = models.CharField(blank=True, max_length=200,
        help_text='Separate multiple sources by comma (must have accompanying URL).')
    source_url = models.URLField('source URL', blank=True,
        help_text='Seperate multile URLs with comma (must have accompanying Source).')
    via = models.CharField(blank=True, max_length=200)
    via_url = models.URLField('via URL', blank=True)

    class Meta:
        ordering = ('parent', 'published')

    def __unicode__(self):
        return '%s Update of "%s"' % (self.date, self.parent.title)