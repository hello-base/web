# -*- coding:utf-8 -*-
from collections import defaultdict
from datetime import date

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timesince
from django.utils.functional import cached_property

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize
from model_utils import FieldTracker
from model_utils.managers import PassThroughManager
from ohashi.db import models as ohashi

from base.apps.accounts.models import ContributorMixin

from .constants import BLOOD_TYPE, CLASSIFICATIONS, PHOTO_SOURCES, SCOPE, STATUS
from .managers import GroupQuerySet, IdolQuerySet, MembershipQuerySet
from .utils import calculate_age


class Person(ContributorMixin):
    name = models.CharField(editable=False, max_length=60)
    family_name = models.CharField(blank=True, max_length=30)
    given_name = models.CharField(blank=True, max_length=30)
    alias = models.CharField(blank=True, max_length=60)

    romanized_name = models.CharField(editable=False, max_length=60)
    romanized_family_name = models.CharField(blank=True, max_length=30)
    romanized_given_name = models.CharField(blank=True, max_length=30)
    romanized_alias = models.CharField(blank=True, max_length=60)

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
        return self._meta.model_name

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class Idol(Person):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(IdolQuerySet)()
    birthdays = ohashi.BirthdayManager()
    tracker = FieldTracker()

    # Status.
    status = models.PositiveSmallIntegerField(choices=STATUS, db_index=True, default=STATUS.active)
    scope = models.PositiveSmallIntegerField(choices=SCOPE, db_index=True, default=SCOPE.hp)

    # Details.
    bloodtype = models.CharField(blank=True, choices=BLOOD_TYPE, default='A', max_length=2)
    height = models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)
    color = models.CharField(blank=True, default='', max_length=7,
        help_text='An idol\'s color. Use a hex value (i.e. #000000).')

    # Dates.
    started = models.DateField(blank=True, db_index=True, null=True,
        help_text='The date this idol joined Hello! Project/became an idol.')
    graduated = models.DateField(blank=True, db_index=True, null=True,
        help_text='The date this idol graduated from Hello! Project.')
    retired = models.DateField(blank=True, db_index=True, null=True,
        help_text='The date this idol retired.')

    # Birth Information.
    birthdate = ohashi.BirthdayField(blank=True, db_index=True, null=True)
    birthplace = models.CharField(blank=True, max_length=200)
    birthplace_romanized = models.CharField(blank=True, max_length=200)
    birthplace_latitude = models.FloatField(blank=True, null=True)
    birthplace_longitude = models.FloatField(blank=True, null=True)

    # Options & Extra Information.
    note = models.TextField(blank=True)

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    photo = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    photo_thumbnail = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    optimized_square = ImageSpecField(source='photo_thumbnail', processors=[SmartResize(width=300, height=300)], format='JPEG', options={'quality': 70})
    optimized_thumbnail = ImageSpecField(source='photo_thumbnail', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})
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

    @property
    def image(self):
        return self.optimized_thumbnail

    def is_gaijin(self):
        return not bool(self.given_name and self.family_name)

    def latest_album(self):
        return self.albums.latest()

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
    groups = models.ManyToManyField('self', blank=True, related_name='supergroups', symmetrical=False)

    # Options & Extra Information.
    former_names = models.CharField(blank=True, max_length=200)
    note = models.TextField(blank=True)

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    photo = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    photo_thumbnail = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    optimized_thumbnail = ImageSpecField(source='photo_thumbnail', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})

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

    @property
    def designation(self):
        if self.designations.exists():
            return self.designations.latest()
        return self

    def designation_for(self, target=None):
        if target and self.designations.exists():
            return self.designations.filter(started__lte=target).filter(Q(ended__gte=target) | Q(ended=None)).get()
        return self

    def generations(self):
        generations = defaultdict(list)
        for membership in self.memberships.select_related('idol'):
            generations[membership.generation].append(membership)
        generations.default_factory = None
        return generations if all(generations) else None

    @property
    def identifier(self):
        return self._meta.model_name

    @property
    def image(self):
        return self.optimized_thumbnail

    def is_active(self, target=None):
        if target:
            return bool(self.started < target and (self.ended is None or self.ended >= target))
        return bool(self.ended is None or self.ended >= date.today())

    def latest_album(self):
        return self.albums.latest()

    def latest_single(self):
        return self.singles.latest()

    def original_members(self):
        return self.members.filter(memberships__started=self.started)

    def final_members(self):
        return self.members.filter(memberships__ended=self.ended)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class Designation(models.Model):
    # A designation a date-based name given to a group, used to handle the
    # complex nature around group name changes in Hello! Project.
    group = models.ForeignKey(Group, related_name='designations')

    # When was the name created/when was it retired?
    started = models.DateField(db_index=True)
    ended = models.DateField(blank=True, db_index=True, null=True)

    # What was the name during that time?
    name = models.CharField(max_length=60)
    romanized_name = models.CharField(max_length=60)

    class Meta:
        get_latest_by = 'started'
        order_with_respect_to = 'group'

    def __unicode__(self):
        return u'%s' % (self.romanized_name)


class Membership(models.Model):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(MembershipQuerySet)()
    tracker = FieldTracker()

    idol = models.ForeignKey(Idol, related_name='memberships')
    group = ohashi.CustomManagerForeignKey(Group, blank=True, null=True, manager=Group.objects.unfiltered, related_name='memberships')

    # Group Involvement Details.
    is_primary = models.BooleanField('Primary?', db_index=True, default=False)
    started = models.DateField(db_index=True)
    ended = models.DateField(blank=True, db_index=True, null=True)
    generation = models.PositiveSmallIntegerField(blank=True, db_index=True, null=True)

    # Leadership Details.
    is_leader = models.BooleanField('Leader?', default=False)
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

    def is_active(self, target=None):
        if target:
            return bool(self.started < target and (self.ended is None or self.ended >= target))
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
    idols = models.ManyToManyField(Idol, blank=True, related_name='%(class)ss')
    groups = models.ManyToManyField(Group, blank=True, related_name='%(class)ss')

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    participating_idols = models.ManyToManyField(Idol, blank=True, related_name='%(class)ss_attributed_to',
        help_text='The remaining idols that are not a member of the given groups.')
    participating_groups = models.ManyToManyField(Group, blank=True, related_name='%(class)ss_attributed_to')

    class Meta:
        abstract = True

    @receiver(post_save)
    def render_participants(sender, instance, created, **kwargs):
        # Being a signal without a sender, we need to make sure models
        # are actually subclasses of ParticipationMixin before we
        # continue.
        if not issubclass(instance.__class__, ParticipationMixin):
            return

        from base.apps.people.models import Membership

        # Do we have existing participants? Clear them out so we can
        # calculate them again.
        instance.participating_idols.clear()
        instance.participating_groups.clear()

        groups = instance.groups.all()
        if groups.exists():
            # If a supergroup is one of the groups attributed, filter out any
            # groups that are a member of that supergroup.
            if instance.supergroup in groups:
                instance.participating_groups.add(instance.supergroup)
                groups = groups.exclude(supergroups__in=[instance.supergroup])

            # Gather all of the individual idol's primary keys
            # attributed to the single into a set().
            idols = instance.idols.all()

            # Specify an empty set() that will contain all of the
            # members of the groups attributed to the single. Then,
            # loop through all of the groups and update the set with
            # all of the individual members' primary keys.
            group_ids = groups.values_list('id', flat=True)
            group_members = Membership.objects.filter(group__in=group_ids).values_list('idol', flat=True)

            # Subtract group_members from idols.
            distinct_idols = idols.exclude(pk__in=group_members)

            # Add the calculated groups and idols to our new list of
            # participating groups and idols.
            instance.participating_groups.add(*list(groups))
            instance.participating_idols.add(*list(distinct_idols))
            return

        # No groups? Just add all the idols.
        instance.participating_idols.add(*list(instance.idols.all()))
        return

    @cached_property
    def supergroup(self):
        for group in self.groups.all():
            if group.classification == CLASSIFICATIONS.supergroup:
                return group


upload_paths = {'groups': 'people/groups/', 'idols': 'people/idols/'}
def get_directory(instance, filename):
    category = instance.category
    return upload_paths.get(category, '')


class Shot(models.Model):
    kind = models.PositiveSmallIntegerField(choices=PHOTO_SOURCES, default=PHOTO_SOURCES.promotional)
    photo = models.ImageField(blank=True, upload_to=get_directory)
    photo_thumbnail = models.ImageField(blank=True, upload_to=get_directory)
    optimized_thumbnail = ImageSpecField(source='photo_thumbnail', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})
    taken = models.DateField()

    class Meta:
        abstract = True
        get_latest_by = 'taken'
        ordering = ('-taken',)

    def __unicode__(self):
        return u'Photo of %s (%s)' % (self.subject.romanized_name, self.taken)

    def save(self, *args, **kwargs):
        super(Shot, self).save(*args, **kwargs)
        latest = self._default_manager.filter(subject=self.subject).latest()
        self.subject.photo = latest.photo
        self.subject.photo_thumbnail = latest.photo_thumbnail
        self.subject.save()


class Groupshot(Shot):
    category = 'groups'
    subject = models.ForeignKey(Group, related_name='photos')


class Headshot(Shot):
    category = 'idols'
    subject = models.ForeignKey(Idol, related_name='photos')
