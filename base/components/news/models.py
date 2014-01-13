# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from itertools import chain

from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from model_utils import Choices

from components.appearances.models import Magazine, Show
from components.correlations.models import Correlation
from components.events.models import Event
from components.merchandise.music.models import Album, Single
from components.people.models import Group, Idol

User = get_user_model()
SUBJECTS = [
    Idol, Group,     # people
    Album, Single,   # merchandise.music
    Event,           # events
    Show, Magazine,  # appearances
]


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

    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_submissions')
    category = models.CharField(choices=CATEGORIES, max_length=16)
    classification = models.CharField(choices=CLASSIFICATION, default=CLASSIFICATION.normal, max_length=16)

    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200)
    body = models.TextField(blank=True)
    published = models.DateField(default=date.today())

    # Happenings.
    correlations = models.ManyToManyField(Correlation, blank=True, null=True, related_name='%(class)ss')

    # Sources.
    source = models.CharField(blank=True, max_length=200,
        help_text='Separate multiple sources by comma (must have accompanying URL).')
    source_url = models.URLField('source URL', blank=True,
        help_text='Seperate multiple URLs with comma (must have accompanying Source).')
    via = models.CharField(blank=True, max_length=200)
    via_url = models.URLField('via URL', blank=True)

    class Meta:
        get_latest_by = 'published'
        ordering = ('-published',)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.published)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'slug': self.slug
        })

    def subjects(self):
        subjects = list(chain((getattr(self, '%ss' % subject._meta.model_name).all() for subject in SUBJECTS)))
        return [subject for sublist in subjects for subject in sublist]


# Involvement.
# In an everlasting effort to not repeat thyself, we create the subject
# foreign keys dynamically. In order to do that, we have to do it outside
# of the initial model specification.
for subject in SUBJECTS:
    Item.add_to_class(
        '%ss' % subject._meta.model_name,
        models.ManyToManyField(subject, blank=True, null=True, related_name='%(class)ss')
    )


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
    body = models.TextField(blank=True)
    published = models.DateField(default=date.today())

    # Sources.
    source = models.CharField(blank=True, max_length=200,
        help_text='Separate multiple sources by comma (must have accompanying URL).')
    source_url = models.URLField('source URL', blank=True,
        help_text='Seperate multiple URLs with comma (must have accompanying Source).')
    via = models.CharField(blank=True, max_length=200)
    via_url = models.URLField('via URL', blank=True)

    class Meta:
        ordering = ('parent', 'published')

    def __unicode__(self):
        return '%s Update of "%s"' % (self.published, self.parent.title)
