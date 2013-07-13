from ohashi.db import models


class Merchandise(models.Model):
    romanized_name = models.CharField()
    name = models.CharField(blank=True)
    released = models.DateField(blank=True)

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
