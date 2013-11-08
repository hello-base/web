from datetime import date

from django.db.models import Q
from django.db.models.query import QuerySet

from .constants import CLASSIFICATIONS, SCOPE, STATUS
from .utils import calculate_average_age


class IdolQuerySet(QuerySet):
    def active(self):
        return self.filter(status=STATUS.active)

    def inactive(self):
        return self.exclude(status=STATUS.active)

    # Convenience Groupings
    def hello_project(self):
        from .models import Group
        groups = Group.objects.hello_project().values_list('id', flat=True)
        return self.filter(primary_membership__group_id__in=groups, primary_membership__ended__isnull=True)

    # Aggregations
    def average_age(self):
        birthdates = self.filter(birthdate__isnull=False).values_list('birthdate', flat=True)
        average_age = calculate_average_age(birthdates)
        return average_age

    def average_height(self):
        heights = self.filter(height__isnull=False).values_list('height', flat=True)
        average_height = round(sum(heights) / len(heights))
        return average_height


class GroupQuerySet(QuerySet):
    def active(self, target=None):
        if target:
            return self.filtered().filter(Q(ended__isnull=True) | Q(ended__gte=target), started__lt=target)
        return self.filtered().filter(Q(ended__isnull=True) | Q(ended__gte=date.today()))

    def inactive(self):
        return self.filtered().filter(ended__lte=date.today())

    def filtered(self):
        return self.exclude(romanized_name='Soloist')

    def unfiltered(self):
        return self.all()

    # Convenience Groupings
    def hello_project(self):
        # Hello Pro Kenshuusei is the only "group" classified as
        # Hello! Project that is not a major group.
        kenshuusei = self.filter(romanized_name='Hello Pro Kenshuusei')
        actives = self.filter(classification=CLASSIFICATIONS.major, scope=SCOPE.hp, status=STATUS.active)
        return (kenshuusei | actives).order_by('started')


class MembershipQuerySet(QuerySet):
    def active(self, for_group=None):
        qs = self.filter(Q(ended__isnull=True) | Q(ended__gte=date.today())).prefetch_related('idol')
        if for_group:
            return qs.filter(group=for_group)
        return qs

    def inactive(self):
        return self.filter(ended__lte=date.today()).prefetch_related('idol')

    def inactive_leaders(self):
        return self.leaders().filter(leadership_ended__lte=date.today())

    def leaders(self):
        return self.filter(is_leader=True).order_by('leadership_started').prefetch_related('idol')
