import datetime
import pytest

from components.merchandise.music.models import Album, Edition, Single, Track
from components.merchandise.music.factories import (AlbumFactory,
    EditionFactory, SingleFactory, TrackFactory)
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

    def test_album_regular_edition(self):
        album = AlbumFactory()
        edition = EditionFactory(album=album, kind=Edition.EDITIONS.regular)
        assert album.regular_edition == edition


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


class TestEditions:
    def test_edition_factory(self):
        single = SingleFactory()
        factory = EditionFactory(single=single)
        assert isinstance(factory, Edition)
        assert 'edition' in factory.romanized_name

    def test_edition_get_absolute_url(self, client):
        single = SingleFactory()
        edition = EditionFactory(single=single)
        response = client.get(edition.get_absolute_url())
        assert edition.get_absolute_url() == single.get_absolute_url()
        assert response.status_code == 200

    def test_edition_parent(self):
        single = SingleFactory()
        edition = EditionFactory(single=single)
        assert edition.parent == single

    def test_get_regular_edition(self):
        single = SingleFactory()
        edition1 = EditionFactory(single=single, kind=Edition.EDITIONS.regular)
        edition2 = EditionFactory(single=single, kind=Edition.EDITIONS.limited)
        assert edition2._get_regular_edition() == edition1


class TestTracks:
    def test_track_factory(self):
        factory = TrackFactory()
        assert isinstance(factory, Track)
        assert 'track' in factory.romanized_name

    def test_track_get_absolute_url(self, client):
        single = SingleFactory()
        factory = TrackFactory(single=single)
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200
