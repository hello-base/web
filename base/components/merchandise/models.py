from datetime import date

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
    uuid = models.UUIDField(auto_add=True)

    class Meta:
        abstract = True
