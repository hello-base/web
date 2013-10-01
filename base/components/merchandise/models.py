from datetime import date

from model_utils import Choices
from model_utils.models import TimeStampedModel
from ohashi.db import models

from components.accounts.models import ContributorMixin
from components.people.models import ParticipationMixin


class Merchandise(ContributorMixin, ParticipationMixin):
    # Shared metadata.
    romanized_name = models.CharField()
    name = models.CharField()
    released = models.DateField(blank=True, db_index=True, default=date.min, null=True)
    price = models.IntegerField(blank=True, null=True)

    # Secondary identifier.
    uuid = models.UUIDField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s' % self.name


class Videodisc(Merchandise):
    """
    An abstract base class for videodisc merchandise. Because of the fundemental
    difference between "concert" discs (which are released to the public) and
    "fan club" discs (which are generally only released to fan club members),
    we cannot consolidate the two into one class.

    """
    class Meta:
        abstract = True


class VideodiscFormat(models.Model):
    """
    An abstract base class for videodiscs. Since disc-based merchandise can
    be released on more than one format, this class covers the specific format
    metadata.

    """
    FORMAT_TYPES = Choices((1, 'dvd', 'DVD'), (2, 'bluray', 'Blu-ray Disc'))

    # Metadata
    kind = models.IntegerField(choices=FORMAT_TYPES, default=FORMAT_TYPES.dvd)
    released = models.DateField(blank=True, db_index=True, default=date.min, null=True)
    catalog_number = models.CharField(blank=True)

    class Meta:
        abstract = True
