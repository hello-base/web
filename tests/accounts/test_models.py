import pytest

from components.accounts.factories import EditorFactory
from components.accounts.models import Editor

pytestmark = pytest.mark.django_db


class TestEditors:
    def test_factory(self):
        factory = EditorFactory()
        assert isinstance(factory, Editor)
        assert 'dancer' in factory.username

    def test_failing_creation(self):
        with pytest.raises(ValueError):
            Editor.objects.create_user(username='')
