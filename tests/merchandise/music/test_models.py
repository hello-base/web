import datetime
import pytest

from components.merchandise.music.models import Album, Edition, Single, Track
from components.merchandise.music.factories import (AlbumFactory,
    EditionFactory, SingleFactory, TrackFactory)
from components.people.factories import GroupFactory

pytestmark = pytest.mark.django_db


class TestAlbums:
    def test_factory(self):
        factory = AlbumFactory()
        assert isinstance(factory, Album)
        assert 'album' in factory.romanized_name
        assert factory.identifier == 'album'

    def test_get_absolute_url(self, client):
        factory = AlbumFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_regular_edition(self):
        album = AlbumFactory()
        edition = EditionFactory(album=album, kind=Edition.EDITIONS.regular)
        assert album.regular_edition == edition

    def test_regular_edition_failure(self):
        # Test that calling `regular_edition` will not fail loudly if the
        # proper edition is not found.
        album = AlbumFactory()
        edition = EditionFactory(album=album, kind=Edition.EDITIONS.limited)
        assert not album.regular_edition

    def test_get_previous_and_next(self):
        album1 = AlbumFactory(romanized_name='album#1', released=datetime.date.today() - datetime.timedelta(days=14), number='1')
        album2 = AlbumFactory(romanized_name='album#2', released=datetime.date.today() - datetime.timedelta(days=7), number='2')
        album3 = AlbumFactory(romanized_name='album#3', released=datetime.date.today())

        group = GroupFactory()
        album1.groups.add(group)
        assert album1.groups.exists()
        album2.groups.add(group)
        assert album2.groups.exists()
        album3.groups.add(group)
        assert album2.groups.exists()

        assert album1.get_next == album2
        assert album2.get_previous == album1
        assert album2.get_next != album3


class TestSingles:
    def test_factory(self):
        factory = SingleFactory()
        assert isinstance(factory, Single)
        assert 'single' in factory.romanized_name
        assert factory.identifier == 'single'

    def test_get_absolute_url(self, client):
        factory = SingleFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_get_previous_and_next(self):
        single1 = SingleFactory(romanized_name='single#1', released=datetime.date.today() - datetime.timedelta(days=14), number='1')
        single2 = SingleFactory(romanized_name='single#2', released=datetime.date.today() - datetime.timedelta(days=7), number='2')
        single3 = SingleFactory(romanized_name='single#3', released=datetime.date.today())

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
    def test_factory(self):
        single = SingleFactory()
        factory = EditionFactory(single=single)
        assert isinstance(factory, Edition)
        assert 'edition' in factory.romanized_name

    def test_get_absolute_url(self, client):
        single = SingleFactory()
        edition = EditionFactory(single=single)
        response = client.get(edition.get_absolute_url())
        assert edition.get_absolute_url() == single.get_absolute_url()
        assert response.status_code == 200

    def test_parent(self):
        single = SingleFactory()
        edition = EditionFactory(single=single)
        assert edition.parent == single

    def test_get_regular_edition(self):
        single = SingleFactory()
        edition1 = EditionFactory(single=single, kind=Edition.EDITIONS.regular)
        edition2 = EditionFactory(single=single, kind=Edition.EDITIONS.limited)
        assert edition2._get_regular_edition() == edition1


class TestTracks:
    def test_factory(self):
        factory = TrackFactory()
        assert isinstance(factory, Track)
        assert 'track' in factory.romanized_name

    def test_get_absolute_url(self, client):
        single = SingleFactory()
        factory = TrackFactory(single=single)
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200
