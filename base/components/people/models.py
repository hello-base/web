# -*- coding:utf-8 -*-
from collections import defaultdict
from datetime import date

from django.core.urlresolvers import reverse
from django.utils import timesince
from django.utils.functional import cached_property

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from model_utils import FieldTracker
from model_utils.managers import PassThroughManager
from ohashi.db import models

from components.accounts.models import ContributorMixin

from .constants import BLOOD_TYPE, CLASSIFICATIONS, PHOTO_SOURCES, SCOPE, STATUS
from .managers import GroupQuerySet, IdolQuerySet, MembershipQuerySet
from .utils import calculate_age


class Person(ContributorMixin):
    name = models.CharField(editable=False, max_length=60)
    romanized_name = models.CharField(editable=False, max_length=60)
    family_name = models.CharField(blank=True, max_length=30)
    given_name = models.CharField(blank=True, max_length=30)
    romanized_family_name = models.CharField(blank=True, max_length=30)
    romanized_given_name = models.CharField(blank=True, max_length=30)
    alias = models.CharField(blank=True, max_length=30)
    romanized_alias = models.CharField(blank=True, max_length=30)
    nicknames = models.CharField(blank=True, max_length=200)
    slug = models.SlugField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def save(self, *args, **kwargs):
        self.name = self._render_name()
        self.romanized_name = self._render_romanized_name()
        super(Person, self).save(*args, **kwargs)

    def _render_name(self):
        if self.alias:
            return u'%s' % (self.alias)
        return u'%s%s' % (self.family_name, self.given_name)

    def _render_romanized_name(self):
        if self.romanized_alias:
            return u'%s' % (self.romanized_alias)
        elif hasattr(self, 'is_gaijin') and self.is_gaijin():
            return u'%s %s' % (self.romanized_given_name, self.romanized_family_name)
        return u'%s %s' % (self.romanized_family_name, self.romanized_given_name)

    @property
    def identifier(self):
        return self._meta.module_name

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class Idol(Person):
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

    # Dates.
    started = models.DateField(db_index=True, null=True,
        help_text='The date this idol joined Hello! Project/became an idol.')
    graduated = models.DateField(blank=True, db_index=True, null=True,
        help_text='The date this idol graduated from Hello! Project.')
    retired = models.DateField(blank=True, db_index=True, null=True,
        help_text='The date this idol retired.')

    # Birth Information.
    birthdate = models.BirthdayField(blank=True, db_index=True, null=True)
    birthplace = models.CharField(blank=True, max_length=200)
    birthplace_romanized = models.CharField(blank=True)
    birthplace_latitude = models.FloatField(blank=True, null=True)
    birthplace_longitude = models.FloatField(blank=True, null=True)

    # Options & Extra Information.
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    photo = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    photo_thumbnail = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    # optimized_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})
    primary_membership = models.ForeignKey('Membership', blank=True, null=True, related_name='primary')

    class Meta:
        ordering = ('birthdate',)

    def get_absolute_url(self):
        return reverse('idol-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super(Idol, self).save(*args, **kwargs)

    @property
    def age(self):
        return calculate_age(self.birthdate)

    def is_gaijin(self):
        return not bool(self.given_name and self.family_name)

    def latest_album(self):
        return self.albums.latest()

    def latest_event(self):
        return self.events.latest()

    def latest_single(self):
        return self.singles.latest()


class Staff(Person):
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'staff'


class Group(ContributorMixin):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(GroupQuerySet)()
    tracker = FieldTracker()

    name = models.CharField(max_length=60)
    romanized_name = models.CharField(max_length=60)
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
    former_names = models.CharField(blank=True, max_length=200)
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    photo = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    photo_thumbnail = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    # optimized_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})

    class Meta:
        ordering = ('started',)

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'slug': self.slug})

    @property
    def age(self):
        if self.ended:
            return calculate_age(self.started, target=self.ended)
        return calculate_age(self.started)

    @property
    def age_in_days(self):
        if self.ended:
            return (self.ended - self.started).days
        return (date.today() - self.started).days

    def generations(self):
        generations = defaultdict(list)
        for membership in self.memberships.select_related('idol'):
            generations[membership.generation].append(membership)
        generations.default_factory = None
        return generations if all(generations) else None

    @property
    def identifier(self):
        return self._meta.module_name

    def is_active(self):
        return bool(self.ended is None or self.ended >= date.today())

    def latest_album(self):
        return self.albums.latest()

    def latest_event(self):
        return self.events.latest()

    def latest_single(self):
        return self.singles.latest()

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


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
    generation = models.PositiveSmallIntegerField(blank=True, db_index=True, null=True)

    # Leadership Details.
    is_leader = models.BooleanField('Leader?')
    leadership_started = models.DateField(blank=True, null=True)
    leadership_ended = models.DateField(blank=True, null=True)

    class Meta:
        get_latest_by = 'started'
        ordering = ('-is_primary', '-started', '-idol__birthdate')
        unique_together = ('idol', 'group')

    def __unicode__(self):
        return '%s (%s)' % (self.idol, self.group.romanized_name)

    def save(self, *args, **kwargs):
        # Denormalize the idol's primary membership.
        super(Membership, self).save(*args, **kwargs)
        if self.is_primary:
            self.idol.primary_membership = self
            self.idol.save()

    def is_active(self):
        return bool(self.ended is None or self.ended >= date.today())

    def days_before_starting(self):
        return (self.started - self.group.started).days

    def days_before_ending(self):
        if self.ended:
            return (self.ended - self.group.started).days

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

    @property
    def standing(self):
        """
        A convenience method that returns a string of a member's
        standing in the given group (e.g., member, former member, etc.).

        """
        former = ''
        if not self.is_active() or self.leadership_ended:
            former = 'former '
        if 'Soloist' in str(self.group):
            standing = 'soloist'
        elif self.is_leader:
            standing = 'leader'
        else:
            standing = 'member'
        return ''.join((former, standing)).capitalize()


class ParticipationMixin(models.Model):
    idols = models.ManyToManyField(Idol, blank=True, null=True, related_name='%(class)ss')
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='%(class)ss')

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    participating_idols = models.ManyToManyField(Idol, blank=True, null=True, related_name='%(class)ss_attributed_to',
        help_text='The remaining idols that are not a member of the given groups.')
    participating_groups = models.ManyToManyField(Group, blank=True, null=True, related_name='%(class)ss_attributed_to')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(ParticipationMixin, self).save(*args, **kwargs)
        from .tasks import render_participants
        render_participants.delay(self)

    @cached_property
    def supergroup(self):
        for group in self.groups.all():
            if group.classification == CLASSIFICATIONS.supergroup:
                return group


class Groupshot(models.Model):
    group = models.ForeignKey(Group, related_name='photos')

    kind = models.PositiveSmallIntegerField(choices=PHOTO_SOURCES, default=PHOTO_SOURCES.promotional)
    photo = models.ImageField(blank=True, upload_to='people/groups/')
    photo_thumbnail = models.ImageField(blank=True, upload_to='people/groups/')
    # optimized_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})
    taken = models.DateField()

    class Meta:
        get_latest_by = 'taken'
        ordering = ('-taken',)

    def __unicode__(self):
        return u'Photo of %s (%s)' % (self.group.romanized_name, self.taken)

    def save(self, *args, **kwargs):
        super(Groupshot, self).save(*args, **kwargs)
        latest = self._default_manager.filter(group=self.group).latest()
        self.group.photo = latest.photo
        self.group.photo_thumbnail = latest.photo_thumbnail
        self.group.save()


class Headshot(models.Model):
    idol = models.ForeignKey(Idol, related_name='photos')

    kind = models.PositiveSmallIntegerField(choices=PHOTO_SOURCES, default=PHOTO_SOURCES.promotional)
    photo = models.ImageField(blank=True, upload_to='people/idols/')
    photo_thumbnail = models.ImageField(blank=True, upload_to='people/idols/')
    # optimized_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})
    taken = models.DateField()

    class Meta:
        get_latest_by = 'taken'
        ordering = ('-taken',)

    def __unicode__(self):
        return u'Photo of %s (%s)' % (self.idol.romanized_name, self.taken)

    def save(self, *args, **kwargs):
        super(Headshot, self).save(*args, **kwargs)
        latest = self._default_manager.filter(idol=self.idol).latest()
        self.idol.photo = latest.photo
        self.idol.photo_thumbnail = latest.photo_thumbnail
        self.idol.save()


class Fact(models.Model):
    idol = models.ForeignKey(Idol, blank=True, null=True, related_name='facts')
    group = models.ForeignKey(Group, blank=True, null=True, related_name='facts')
    body = models.TextField()

    def __unicode__(self):
        return u'%s: %s...' % (self.parent.romanized_name, self.body[:40])

    @property
    def parent(self):
        return filter(None, [self.idol, self.group])[0]
