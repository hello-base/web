from datetime import date

from ohashi.db import models


class Merchandise(models.Model):
    idols = models.ManyToManyField('people.Idol', blank=True, null=True, related_name='%(class)ss')
    groups = models.ManyToManyField('people.Group', blank=True, null=True, related_name='%(class)ss')

    romanized_name = models.CharField()
    name = models.CharField(blank=True)
    released = models.DateField(blank=True, db_index=True, default=date.min, null=True)

    # Secondary Identifier
    uuid = models.UUIDField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s' % self.name


class DVD(Merchandise):
    """
    An abstract base class for DVD merchandise. Because of the fundemental
    difference between "concert" DVDs (which are released to the public) and
    "fan club" DVDs (which are generally only released to fan club members),
    we cannot consolidate the two into one class.

    """
    class Meta:
        abstract = True
