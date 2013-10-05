from django.test import TestCase

from components.base.merchandise.music.factories import (AlbumFactory,
    BaseFactory, EditionFactory, SingleFactory)


class TestAlbums(TestCase):
    def test_album_factory(self):
        album = AlbumFactory()
        assert isinstance(album, Album)

    def test_album_creation(self):
        album = AlbumFactory()
        assert 'album' in album.romanized_name


class TestSingles(TestCase):
    def test_single_factory(self):
        single = SingleFactory()
        assert isinstance(single, Single)

    def test_single_creation(self):
        single = SingleFactory()
        assert 'single' in single.romanized_name
