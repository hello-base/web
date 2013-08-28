from datetime import date

from django.core.urlresolvers import reverse

from model_utils import FieldTracker
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from ohashi.db import models

from .constants import (BLOOD_TYPE, CLASSIFICATIONS, SCOPE, STATUS)
from .managers import GroupQuerySet, IdolQuerySet, MembershipQuerySet
from .utils import calculate_age, calculate_average_age


class Person(TimeStampedModel):
    name = models.CharField(editable=False)
    romanized_name = models.CharField(editable=False)
    family_name = models.CharField(blank=True)
    given_name = models.CharField(blank=True)
    romanized_family_name = models.CharField(blank=True)
    romanized_given_name = models.CharField(blank=True)
    alias = models.CharField(blank=True)
    romanized_alias = models.CharField(blank=True)
    nicknames = models.CharField(blank=True)
    slug = models.SlugField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.romanized_name)


class Idol(Person):
    GAIJINS = ['April', 'Chelsea', 'Danielle', 'Lehua', 'Mika Taressa']

    # Model Managers.
    objects = PassThroughManager.for_queryset_class(IdolQuerySet)()
    birthdays = models.BirthdayManager()
    tracker = FieldTracker()

    # Status.
    status = models.PositiveSmallIntegerField(choices=STATUS, db_index=True, default=STATUS.active)
    scope = models.PositiveSmallIntegerField(choices=SCOPE, db_index=True, default=SCOPE.hp)

    # Details.
    bloodtype = models.CharField(blank=True, choices=BLOOD_TYPE, default='A', max_length=2)
    height = models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)

    # Birth Information.
    birthdate = models.BirthdayField(blank=True, db_index=True, null=True)
    birthplace = models.CharField(blank=True)
    birthplace_romanized = models.CharField(blank=True)
    birthplace_latitude = models.FloatField(blank=True, null=True)
    birthplace_longitude = models.FloatField(blank=True, null=True)

    # Options & Extra Information.
    has_discussions = models.BooleanField('activate discussions for this idol.', default=False)
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    def get_absolute_url(self):
        return reverse('idol-detail', kwargs={'slug': self.slug})

    def age(self):
        return calculate_age(self.birthdate)

    def latest_album(self):
        return self.albums.latest()

    def latest_single(self):
        return self.singles.latest()

    def primary_group(self):
        return self.memberships.select_related('group').get(is_primary=True)


class Staff(Person):
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'staff'


class Group(TimeStampedModel):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(GroupQuerySet)()
    tracker = FieldTracker()

    name = models.CharField()
    romanized_name = models.CharField()
    slug = models.SlugField()

    # Status.
    classification = models.PositiveSmallIntegerField(choices=CLASSIFICATIONS, db_index=True, default=CLASSIFICATIONS.major)
    status = models.PositiveSmallIntegerField(choices=STATUS, db_index=True, default=STATUS.active)
    scope = models.PositiveSmallIntegerField(choices=SCOPE, db_index=True, default=SCOPE.hp)

    # Details.
    started = models.DateField(db_index=True)
    ended = models.DateField(blank=True, db_index=True, null=True)
    members = models.ManyToManyField(Idol, related_name='groups', through='Membership')

    # Parents & Children.
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subgroups')
    groups = models.ManyToManyField('self', blank=True, null=True, related_name='member_groups', symmetrical=False)

    # Options & Extra Information.
    has_discussions = models.BooleanField('activate discussions for this group.', default=False)
    former_names = models.CharField(blank=True)
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'slug': self.slug})

    def age_in_days(self):
        if self.ended:
            return (self.ended - self.started).days
        return (date.today() - self.started).days

    def latest_album(self):
        return self.albums.latest()

    def latest_single(self):
        return self.singles.latest()


class Membership(models.Model):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(MembershipQuerySet)()
    tracker = FieldTracker()

    idol = models.ForeignKey(Idol, related_name='memberships')
    group = models.CustomManagerForeignKey(Group, blank=True, null=True, manager=Group.objects.unfiltered, related_name='memberships')

    # Group Involvement Details.
    is_primary = models.BooleanField('Primary?', db_index=True, default=False)
    started = models.DateField(db_index=True)
    ended = models.DateField(blank=True, db_index=True, null=True)

    # Leadership Details.
    is_leader = models.BooleanField('Is/Was leader?')
    leadership_started = models.DateField(blank=True, null=True)
    leadership_ended = models.DateField(blank=True, null=True)

    class Meta:
        get_latest_by = 'started'
        ordering = ('-is_primary', '-started', '-idol__birthdate')
        unique_together = ('idol', 'group')

    def __unicode__(self):
        if self.group.name == 'Soloist':
            return '%s (Soloist)' % (self.idol)
        return '%s (member of %s)' % (self.idol, self.group.name)

    def is_active(self):
        if self.ended is None or self.ended >= date.today():
            return True
        return False

    def tenure_in_days(self):
        if self.ended:
            return (self.ended - self.started).days
        return (date.today() - self.started).days

    def days_before_becoming_leader(self):
        if self.is_leader:
            return (self.leadership_started - self.group.started).days

    def leadership_tenure(self):
        if self.is_leader:
            if self.leadership_ended:
                return timesince.timesince(self.leadership_started, now=self.leadership_ended)
            return timesince.timesince(self.leadership_started, now=date.today())

    def leadership_tenure_in_days(self):
        if self.is_leader:
            if self.leadership_ended:
                return (self.leadership_ended - self.leadership_started).days
            return (date.today() - self.leadership_started).days


class Trivia(models.Model):
    idol = models.ForeignKey(Idol, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)

    # Information
    body = models.TextField()

    def __unicode__(self):
        if self.idol:
            return u'%s trivia' % self.idol.romanized_name
        if self.group:
            return u'%s trivia' % self.group.romanized_name
        if self.idol and self.group:
            return u'%s trivia (%s)' % (self.group.romanized_name, self.idol.romanized_name)
        return u'trivia'
    # If multiple idols/groups are named in trivia, how do you return multiple idol/group names?
