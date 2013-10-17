import datetime
import pytest

from components.merchandise.music.models import Album, Single
from components.merchandise.music.factories import (AlbumFactory,
    BaseFactory, SingleFactory)
from components.people.factories import GroupFactory


pytestmark = pytest.mark.django_db

class TestAlbums:
    def test_album_factory(self):
        factory = AlbumFactory()
        assert isinstance(factory, Album)
        assert 'album' in factory.romanized_name
        assert factory.identifier == 'album'

    def test_album_get_absolute_url(self, client):
        factory = AlbumFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200


class TestSingles:
    def test_single_factory(self):
        factory = SingleFactory()
        assert isinstance(factory, Single)
        assert 'single' in factory.romanized_name
        assert factory.identifier == 'single'

    def test_single_get_absolute_url(self, client):
        factory = SingleFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_single_get_previous_and_next(self):
        single1 = SingleFactory(romanized_name='single1', released=datetime.date.today() - datetime.timedelta(days=14), number='1')
        single2 = SingleFactory(romanized_name='single2', released=datetime.date.today() - datetime.timedelta(days=7), number='2')
        single3 = SingleFactory(romanized_name='single2', released=datetime.date.today())

        group = GroupFactory()
        single1.groups.add(group)
        assert single1.groups.exists()
        single2.groups.add(group)
        assert single2.groups.exists()
        single3.groups.add(group)
        assert single2.groups.exists()

        assert single1.get_next == single2
        assert single2.get_previous == single1
        assert single2.get_next != single3
