from django.db import models

from components.accounts.models import Editor

class News(models.Model)
    CATEGORIES = Choices(
            ('announcement', 'Announcement'),
            ('appearance', 'Appearance'),
            ('audition', 'Audition'),
            ('event', 'Event'),
            ('goods', 'Goods'),
            ('graduation', 'Graduation'),
            ('musicvideo', 'Preview'),
            ('release', 'Release'),
            ('other', 'Other'),
        )
    category = models.CharField(choices=CATEGORIES, max_length=16)
    title = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    body = models.TextField(blank=True)
    author = models.ForeignKey(Editor, blank=True, null=True, related_name='%(class)s_submissions')

    # Involvement.
    idols = models.ManyToManyField(Idol, blank=True, null=True, related_name='%(class)ss')
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='%(class)ss')
    release = models.ManyToManyField(Merchandise, blank=True, null=True, related_name='%ses')
    events = models.ManyToManyField(Event, blank=True, null=True, related_name='%(class)ss')

    # Sources.
    source = models.CharField(max_length=200)
    source_url = models.URLField(blank=True)
    via = models.CharField(max_length=200, blank=True)
    via_url = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.date)


class Update(models.Model)
    parent = models.ForeignKey(News, related_name='updates')
    date = models.DateField(auto_now_add=True)
    body = models.TextField(blank=True)
    author = models.ForeignKey(Editor, blank=True, null=True, related_name='%(class)s_submissions')

    # Sources.
    source = models.CharField(max_length=200)
    source_url = models.URLField(blank=True)
    via = models.CharField(max_length=200, blank=True)
    via_url = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s Update of "%s"' % (self.date, self.parent.title)