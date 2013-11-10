import datetime
import pytest

from django.core.exceptions import ValidationError

from components.merchandise.music.models import (Album, Edition, Single, Track,
    Video)
from components.merchandise.music.factories import (AlbumFactory,
    EditionFactory, SingleFactory, TrackFactory, TrackOrderFactory,
    VideoFactory)
from components.people.constants import CLASSIFICATIONS
from components.people.factories import (GroupFactory, MembershipFactory,
    IdolFactory)

edition_type = Edition.EDITIONS
video_type = Video.VIDEO_TYPES
pytestmark = pytest.mark.django_db


class TestParticipations:
    # While this code lives in `components.people.models,` it is tested here
    # because it is a mixin that nearly all of the music models use.
    @pytest.fixture
    def release(self):
        return SingleFactory()

    def test_render_idols(self, release):
        release.idols.add(*[IdolFactory() for i in xrange(5)])
        release.save()
        assert len(release.participating_idols.all()) == 5
        assert not release.participating_groups.all()

        # Run it again to make sure the participating_* relations are cleared
        # on a second run-through.
        release.idols.clear()
        release.idols.add(*[IdolFactory() for i in xrange(3)])
        release.save()
        assert len(release.participating_idols.all()) == 3
        assert not release.participating_groups.all()

    def test_render_group(self, release):
        group = GroupFactory()
        idols = [IdolFactory() for i in xrange(3)]
        [MembershipFactory(group=group, idol=idols[i]) for i in xrange(3)]
        release.groups.add(group)
        release.idols.add(*idols)
        release.save()
        assert len(release.participating_groups.all()) == 1
        assert not release.participating_idols.all()

    def test_render_supergroup(self, release):
        supergroup = GroupFactory(classification=CLASSIFICATIONS.supergroup)
        groups = [GroupFactory() for i in xrange(3)]
        release.groups.add(supergroup)
        release.groups.add(*groups)
        release.save()
        assert len(release.participating_groups.all()) == 1
        assert release.participating_groups.all()[0] == supergroup
        assert not release.participating_idols.all()


class TestAlbums:
    def test_factory(self):
        factory = AlbumFactory()
        assert isinstance(factory, Album)
        assert 'album' in factory.romanized_name
        assert factory.identifier == 'album'

    def test_save_with_regular_edition_data(self):
        factory = AlbumFactory()
        regular_edition = EditionFactory(
            album=factory,
            kind=edition_type.regular,
            art='/path/to/art-regular.png',
            released=datetime.date.today()
        )
        factory.save()
        assert factory.regular_edition == regular_edition
        assert factory.art == regular_edition.art
        assert factory.released == regular_edition.released

    def test_save_with_digital_edition_data(self):
        factory = AlbumFactory()
        digital_edition = EditionFactory(
            album=factory,
            kind=edition_type.digital,
            art='/path/to/art-digital.png',
            released=datetime.date.today()
        )
        factory.save()
        assert factory.digital_edition == digital_edition
        assert factory.art == digital_edition.art
        assert factory.released == digital_edition.released

    def test_get_absolute_url(self, client):
        factory = AlbumFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_digital_edition(self):
        album = AlbumFactory()
        edition = EditionFactory(album=album, kind=edition_type.digital)
        assert album.digital_edition == edition

    def test_regular_edition(self):
        album = AlbumFactory()
        edition = EditionFactory(album=album, kind=edition_type.regular)
        assert album.regular_edition == edition

    def test_regular_edition_failure(self):
        # Test that calling `regular_edition` will not fail loudly if the
        # proper edition is not found.
        album = AlbumFactory()
        edition = EditionFactory(album=album, kind=edition_type.limited)
        assert edition in album.editions.all()
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
        assert not album1.get_previous
        assert not album3.get_next


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
        assert not single1.get_previous
        assert not single3.get_next


class TestEditions:
    def test_factory(self):
        single = SingleFactory()
        factory = EditionFactory(single=single)
        assert isinstance(factory, Edition)
        assert 'edition' in factory.romanized_name

    def test_save(self):
        single = SingleFactory()
        edition = EditionFactory(single=single, kind=edition_type.regular, art='/path/to/art-regular.png')
        assert single.art == edition.art

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
        edition1 = EditionFactory(single=single, kind=edition_type.regular)
        edition2 = EditionFactory(single=single, kind=edition_type.limited)
        assert edition2._get_regular_edition() == edition1

    def test_participants(self):
        single = SingleFactory()
        groups = [GroupFactory() for i in xrange(3)]
        single.groups.add(*groups)
        single.save()

        edition = EditionFactory(single=single)
        assert len(edition.participants()) == 3

    def test_render_tracklist_for_empty_editions(self):
        single = SingleFactory()
        regular = EditionFactory(single=single, kind=edition_type.regular)
        limited = EditionFactory(single=single, kind=edition_type.limited)
        [TrackOrderFactory(position=i + 1, edition=regular) for i in xrange(3)]
        assert list(limited.tracklist) == list(regular.tracklist)

    def test_eventv_tracklist(self):
        edition = EditionFactory(kind=edition_type.eventv)
        assert not edition.tracklist

    def test_singlev_tracklist(self):
        edition = EditionFactory(kind=edition_type.singlev)
        assert not edition.tracklist


class TestTracks:
    def test_factory(self):
        factory = TrackFactory()
        assert isinstance(factory, Track)
        assert 'track' in factory.romanized_name

    def test_get_absolute_url(self, client):
        single = SingleFactory()
        original_track = TrackFactory(single=single)
        response = client.get(original_track.get_absolute_url())
        assert response.status_code == 200

        child_track = TrackFactory(single=single, original_track=original_track)
        response = client.get(child_track.get_absolute_url())
        assert child_track.get_absolute_url() == original_track.get_absolute_url()
        assert response.status_code == 200

    def test_original_track_slug_exception(self):
        with pytest.raises(ValidationError):
            TrackFactory(original_track=TrackFactory(slug='track'), slug='track')


class TestVideos:
    def test_factory(self):
        factory = VideoFactory()
        assert isinstance(factory, Video)
        assert 'video' in factory.romanized_name

    def test_parent(self):
        single = SingleFactory()
        factory = VideoFactory(single=single)
        assert factory.parent == single

    def test_rendered_kind_display(self):
        music = VideoFactory(kind=video_type.pv_regular)
        assert music.rendered_kind_display == 'Music Video'

        making = VideoFactory(kind=video_type.making_general)
        assert making.rendered_kind_display == 'Making of'

        performance = VideoFactory(kind=video_type.bonus_performance)
        assert performance.rendered_kind_display == 'Performance'

        other = VideoFactory(kind=video_type.other)
        assert other.rendered_kind_display == ''
