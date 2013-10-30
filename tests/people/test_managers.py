import pytest

from components.people.factories import IdolFactory
from components.people.models import Idol
from components.people.constants import STATUS

pytestmark = pytest.mark.django_db


class TestIdols:
    @pytest.fixture
    def idols(self):
        idols = []
        [idols.append(IdolFactory(status=STATUS.active)) for i in xrange(3)]
        [idols.append(IdolFactory(status=STATUS.former)) for i in xrange(2)]
        return idols

    def test_active_manager(self, idols):
        assert len(Idol.objects.active()) == 3

    def test_inactive_manager(self, idols):
        assert len(Idol.objects.inactive()) == 2
