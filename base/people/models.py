from django.db import models

from model_utils import ModelTracker
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel

from .constants import (BLOOD_TYPE, CLASSIFICATIONS, SCOPE, STATUS)


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


class Idol(Person):
    GAIJINS = ['April', 'Chelsea', 'Danielle', 'Lehua', 'Mika Taressa']

    # Status
    status = models.PositiveSmallIntegerField(choices=STATUS, db_index=True, default=STATUS.active)
    scope = models.PositiveSmallIntegerField(choices=SCOPE, db_index=True, default=SCOPE.hp)

    # Details
    bloodtype = models.CharField(blank=True, choices=BLOOD_TYPE, default='A', max_length=2)
    height = models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)

    # Birth Information
    birthdate = models.BirthdayField(blank=True, db_index=True, null=True)
    birthplace = models.CharField(blank=True)
    birthplace_romanized = models.CharField(blank=True)
    birthplace_latitude = models.FloatField(blank=True, null=True)
    birthplace_longitude = models.FloatField(blank=True, null=True)

    # Options & Extra Information
    has_discussions = models.BooleanField('activate discussions for this idol.', default=False)
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    # Denormalized Headshot & ImageKit Specifications
    photo = models.ImageField(blank=True, editable=False, upload_to='people/idols/')
    display = specs.ImageSpec([Adjust(contrast=1.1, sharpness=1.1), ResizeToFit(width=296)], image_field='photo', options={'quality': 90})
    thumbnail = specs.ImageSpec([Adjust(contrast=1.1, sharpness=1.1), ResizeToFit(width=144)], image_field='photo', options={'quality': 90})
    mini = specs.ImageSpec([Adjust(contrast=1.1, sharpness=1.1), SmartCrop(60, 60)], image_field='photo', options={'quality': 90})

    # Model Managers
    objects = PassThroughManager.for_queryset_class(IdolQuerySet)()
    birthdays = models.BirthdayManager()
    tracker = ModelTracker()


class Group(TimeStampedModel):
    name = models.CharField()
    romanized_name = models.CharField()
    slug = models.SlugField()

    # Status
    classification = models.PositiveSmallIntegerField(choices=CLASSIFICATIONS, db_index=True, default=CLASSIFICATIONS.major)
    status = models.PositiveSmallIntegerField(choices=STATUS, db_index=True, default=STATUS.active)
    scope = models.PositiveSmallIntegerField(choices=SCOPE, db_index=True, default=SCOPE.hp)

    # Details
    started = models.DateField(db_index=True)
    ended = models.DateField(blank=True, db_index=True, null=True)
    members = models.ManyToManyField(Idol, related_name='groups', through='Membership')

    # Parents & Children
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subgroups')
    groups = models.ManyToManyField('self', blank=True, null=True, related_name='member_groups', symmetrical=False)

    # Options & Extra Information
    has_discussions = models.BooleanField('activate discussions for this group.', default=False)
    former_names = models.CharField(blank=True)
    note = models.TextField(blank=True)
    note_processed = models.TextField(blank=True, editable=False)

    # Model Managers
    tracker = ModelTracker()


class Membership(models.Model):
    idol = models.ForeignKey(Idol, related_name='memberships')
    group = models.CustomManagerForeignKey(Group, blank=True, null=True, manager=Group.objects.unfiltered, related_name='memberships')

    # Group Involvement Details
    is_primary = models.BooleanField('Primary?', db_index=True, default=False)
    started = models.DateField(db_index=True)
    ended = models.DateField(blank=True, db_index=True, null=True)

    # Leadership Details
    is_leader = models.BooleanField('Is/Was leader?')
    leadership_started = models.DateField(blank=True, null=True)
    leadership_ended = models.DateField(blank=True, null=True)

    # Model Managers
    objects = PassThroughManager.for_queryset_class(MembershipQuerySet)()
    tracker = ModelTracker()


class Trivia(models.Model):
    idol = models.ForeignKey(Idol, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)

    # Information
    body = models.TextField()

    def __unicode__(self):
        if self.idol:
            return u'%s trivia' self.idol.romanized_name
        if self.group:
            return u'%s trivia' self.group.romanized_name
        if self.idol and self.group:
            return u'%s trivia (%s)' % (self.group.romanized_name, self.idol.romanized_name)
        return u'trivia'
    # If multiple idols/groups are named in trivia, how do you return multiple idol/group names?
