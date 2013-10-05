from django.test import TestCase

from components.merchandise.music.factories import (AlbumFactory,
    BaseFactory, SingleFactory)


class TestAlbums(TestCase):
    def test_album_factory(self):
        album = AlbumFactory()
        assert isinstance(album, Album)

    def test_album_creation(self):
        album = AlbumFactory()
        assert 'album' in album.romanized_name

    def test_album_identifier(self):
        album = AlbumFactory()
        assert album.identifier == 'album'


class TestSingles(TestCase):
    def test_single_factory(self):
        single = SingleFactory()
        assert isinstance(single, Single)

    def test_single_creation(self):
        single = SingleFactory()
        assert 'single' in single.romanized_name

    def test_single_identifier(self):
        single = SingleFactory()
        assert single.identifier == 'single'
