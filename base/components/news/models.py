from django.db import models
from django.contrib.auth import get_user_model

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

    category = models.CharField(choices=CATEGORIES, max_length=16)
    title = models.CharField(max_length=500)
    date = models.DateField()
    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_submissions')
    body = models.TextField(blank=True)

    # Involvement.
    idols = models.ManyToManyField(Idol, blank=True, null=True, related_name='%(class)ss')
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='%(class)ss')
    singles = models.ManyToManyField(Single, blank=True, null=True, related_name='%(class)ss')
    albums = models.ManyToManyField(Album, blank=True, null=True, related_name='%(class)ss')
    events = models.ManyToManyField(Event, blank=True, null=True, related_name='%(class)ss')

    # Sources.
    source = models.CharField(max_length=200, blank=True, help_text='Separate multiple sources by comma (must have accompanying URL).')
    source_url = models.URLField(blank=True, help_text='Seperate multile URLs with comma (must have accompanying Source).')
    via = models.CharField(max_length=200, blank=True)
    via_url = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.date)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images')

    image = models.ImageField(blank=True, upload_to='news/')
    caption = models.TextField(blank=True)
    optimized_thumbnail = ImageSpecField(source='photo_thumbnail', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})


class Update(models.Model):
    parent = models.ForeignKey(Item, related_name='updates')
    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_submissions')
    date = models.DateField()
    body = models.TextField(blank=True)

    # Sources.
    source = models.CharField(max_length=200, blank=True)
    source_url = models.URLField(blank=True)
    via = models.CharField(max_length=200, blank=True)
    via_url = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s Update of "%s"' % (self.date, self.parent.title)
