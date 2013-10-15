from datetime import date

from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timesince
from django.utils.functional import cached_property

from model_utils import FieldTracker
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from ohashi.db import models

from .constants import (BLOOD_TYPE, CLASSIFICATIONS, PHOTO_SOURCES,
    SCOPE, STATUS)
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
        elif hasattr(self, 'is_gaijin'):
            if self.is_gaijin():
                return u'%s %s' % (self.romanized_given_name, self.romanzied_family_name)
        return u'%s %s' % (self.romanized_family_name, self.romanized_given_name)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


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
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    photo = models.ImageField(blank=True, upload_to='people/%(class)ss/')
    primary_membership = models.ForeignKey('Membership', blank=True, null=True, related_name='primary')

    class Meta:
        ordering = ('birthdate',)

    def get_absolute_url(self):
        return reverse('idol-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Denormalize the idol's primary membership. Make sure that
        # primary membership exists first.
        try:
            self.primary_membership = self.memberships.get(is_primary=True)
        except Membership.DoesNotExist:
            pass
        return super(Idol, self).save(*args, **kwargs)

    def age(self):
        return calculate_age(self.birthdate)

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
    former_names = models.CharField(blank=True)
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    photo = models.ImageField(blank=True, upload_to='people/%(class)ss/')

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'slug': self.slug})

    def age(self):
        if self.ended:
            return calculate_age(self.started, target=self.ended)
        return calculate_age(self.started)

    def age_in_days(self):
        if self.ended:
            return (self.ended - self.started).days
        return (date.today() - self.started).days

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')

    def is_active(self):
        if self.ended is None or self.ended >= date.today():
            return True
        return False

    def is_gaijin(self):
        return self.given_name in self.GAIJINS

    def latest_album(self):
        return self.albums.latest()

    def latest_event(self):
        return self.events.latest()

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
        if self.group.romanized_name == 'Soloist':
            return '%s (Soloist)' % (self.idol)
        return '%s (member of %s)' % (self.idol, self.group.romanized_name)

    def is_active(self):
        if self.ended is None or self.ended >= date.today():
            return True
        return False

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
        if self.group_id == 65: # Soloist
            if self.ended:
                return 'Former soloist'
            return 'Soloist'

        if self.is_leader:
            if self.leadership_ended:
                return 'Former leader'
            return 'Current leader'
        else:
            if self.ended:
                return 'Former member'
            return 'Member'


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

    @receiver(post_save)
    def render_participants(sender, instance, created, **kwargs):
        # Being a signal without a sender, we need to make sure models
        # are actually subclasses of ParticipationMixin before we
        # continue.
        if not issubclass(instance.__class__, ParticipationMixin):
            return

        from components.people.models import Idol, Membership

        # Do we have existing participants? Clear them out so we can
        # calculate them again.
        instance.participating_idols.clear()
        instance.participating_groups.clear()

        groups = instance.groups.all()
        if groups.exists():
            # If a supergroup is one of the groups attributed, just
            # show the supergroup.
            if instance.supergroup in groups:
                return instance.participating_groups.add(instance.supergroup)

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


class Groupshot(models.Model):
    group = models.ForeignKey(Group, related_name='photos')

    kind = models.PositiveSmallIntegerField(choices=PHOTO_SOURCES, default=PHOTO_SOURCES.promotional)
    photo = models.ImageField(upload_to='people/groups/')
    taken = models.DateField()

    class Meta:
        get_latest_by = 'taken'
        ordering = ('-taken',)

    def __unicode__(self):
        return u'Photo of %s (%s)' % (self.group.name, self.taken)

    def save(self, *args, **kwargs):
        super(Groupshot, self).save(*args, **kwargs)
        if self.kind:
            photo = self.objects.latest()
            self.group.photo = photo
            self.group.save()


class Headshot(models.Model):
    idol = models.ForeignKey(Idol, related_name='photos')

    kind = models.PositiveSmallIntegerField(choices=PHOTO_SOURCES, default=PHOTO_SOURCES.promotional)
    photo = models.ImageField(upload_to='people/idols/')
    taken = models.DateField()

    class Meta:
        get_latest_by = 'taken'
        ordering = ('-taken',)

    def __unicode__(self):
        return u'Photo of %s (%s)' % (self.idol.name, self.taken)

    def save(self, *args, **kwargs):
        super(Headshot, self).save(*args, **kwargs)
        if self.id:
            photo = self.objects.latest()
            self.idol.photo = photo
            self.idol.save()
