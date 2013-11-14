# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Track', fields ['uuid']
        db.delete_unique(u'music_track', ['uuid'])

        # Removing unique constraint on 'Single', fields ['uuid']
        db.delete_unique(u'music_single', ['uuid'])

        # Removing unique constraint on 'Album', fields ['uuid']
        db.delete_unique(u'music_album', ['uuid'])


        # Changing field 'Album.name'
        db.alter_column(u'music_album', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Album.number'
        db.alter_column(u'music_album', 'number', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'Album.romanized_name'
        db.alter_column(u'music_album', 'romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Album.slug'
        db.alter_column(u'music_album', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'Album.uuid'
        db.alter_column(u'music_album', 'uuid', self.gf('django.db.models.fields.CharField')(max_length=36))

        # Changing field 'Video.name'
        db.alter_column(u'music_video', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Video.video_url'
        db.alter_column(u'music_video', 'video_url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Video.romanized_name'
        db.alter_column(u'music_video', 'romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Edition.name'
        db.alter_column(u'music_edition', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Edition.romanized_name'
        db.alter_column(u'music_edition', 'romanized_name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Edition.catalog_number'
        db.alter_column(u'music_edition', 'catalog_number', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Changing field 'Single.name'
        db.alter_column(u'music_single', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Single.number'
        db.alter_column(u'music_single', 'number', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'Single.romanized_name'
        db.alter_column(u'music_single', 'romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Single.slug'
        db.alter_column(u'music_single', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'Single.uuid'
        db.alter_column(u'music_single', 'uuid', self.gf('django.db.models.fields.CharField')(max_length=36))

        # Changing field 'Track.romanized_name_alternate'
        db.alter_column(u'music_track', 'romanized_name_alternate', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Track.name'
        db.alter_column(u'music_track', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Track.translated_name'
        db.alter_column(u'music_track', 'translated_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Track.name_alternate'
        db.alter_column(u'music_track', 'name_alternate', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Track.romanized_name'
        db.alter_column(u'music_track', 'romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Track.slug'
        db.alter_column(u'music_track', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'Track.uuid'
        db.alter_column(u'music_track', 'uuid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True))

        # Changing field 'Label.romanized_name'
        db.alter_column(u'music_label', 'romanized_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Label.slug'
        db.alter_column(u'music_label', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'Label.name'
        db.alter_column(u'music_label', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Album.name'
        db.alter_column(u'music_album', 'name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Album.number'
        db.alter_column(u'music_album', 'number', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Album.romanized_name'
        db.alter_column(u'music_album', 'romanized_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Album.slug'
        db.alter_column(u'music_album', 'slug', self.gf('ohashi.db.models.fields.SlugField')())

        # Changing field 'Album.uuid'
        db.alter_column(u'music_album', 'uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')(auto_add=True))
        # Adding unique constraint on 'Album', fields ['uuid']
        db.create_unique(u'music_album', ['uuid'])


        # Changing field 'Video.name'
        db.alter_column(u'music_video', 'name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Video.video_url'
        db.alter_column(u'music_video', 'video_url', self.gf('ohashi.db.models.fields.URLField')())

        # Changing field 'Video.romanized_name'
        db.alter_column(u'music_video', 'romanized_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Edition.name'
        db.alter_column(u'music_edition', 'name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Edition.romanized_name'
        db.alter_column(u'music_edition', 'romanized_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Edition.catalog_number'
        db.alter_column(u'music_edition', 'catalog_number', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Single.name'
        db.alter_column(u'music_single', 'name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Single.number'
        db.alter_column(u'music_single', 'number', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Single.romanized_name'
        db.alter_column(u'music_single', 'romanized_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Single.slug'
        db.alter_column(u'music_single', 'slug', self.gf('ohashi.db.models.fields.SlugField')())

        # Changing field 'Single.uuid'
        db.alter_column(u'music_single', 'uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')(auto_add=True))
        # Adding unique constraint on 'Single', fields ['uuid']
        db.create_unique(u'music_single', ['uuid'])


        # Changing field 'Track.romanized_name_alternate'
        db.alter_column(u'music_track', 'romanized_name_alternate', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Track.name'
        db.alter_column(u'music_track', 'name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Track.translated_name'
        db.alter_column(u'music_track', 'translated_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Track.name_alternate'
        db.alter_column(u'music_track', 'name_alternate', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Track.romanized_name'
        db.alter_column(u'music_track', 'romanized_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Track.slug'
        db.alter_column(u'music_track', 'slug', self.gf('ohashi.db.models.fields.SlugField')())

        # Changing field 'Track.uuid'
        db.alter_column(u'music_track', 'uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')(auto_add=True, null=True))
        # Adding unique constraint on 'Track', fields ['uuid']
        db.create_unique(u'music_track', ['uuid'])


        # Changing field 'Label.romanized_name'
        db.alter_column(u'music_label', 'romanized_name', self.gf('ohashi.db.models.fields.CharField')())

        # Changing field 'Label.slug'
        db.alter_column(u'music_label', 'slug', self.gf('ohashi.db.models.fields.SlugField')())

        # Changing field 'Label.name'
        db.alter_column(u'music_label', 'name', self.gf('ohashi.db.models.fields.CharField')())

    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 13, 0, 0)', 'blank': 'True'}),
            'base_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'email': ('ohashi.db.models.fields.EmailField', [], {'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'refresh_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'token_expiration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'username': ('ohashi.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True'})
        },
        u'music.album': {
            'Meta': {'ordering': "('-released',)", 'object_name': 'Album'},
            'art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_compilation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'to': u"orm['music.Label']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'album_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'music.edition': {
            'Meta': {'ordering': "('kind', 'romanized_name')", 'object_name': 'Edition'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'editions'", 'null': 'True', 'to': u"orm['music.Album']"}),
            'art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'single': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'editions'", 'null': 'True', 'to': u"orm['music.Single']"}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'editions'", 'to': u"orm['music.Track']", 'through': u"orm['music.TrackOrder']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'editions'", 'to': u"orm['music.Video']", 'through': u"orm['music.VideoTrackOrder']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'music.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'music.single': {
            'Meta': {'ordering': "('-released',)", 'object_name': 'Single'},
            'art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'has_8cm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_cassette': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_lp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_indie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'singles'", 'null': 'True', 'to': u"orm['music.Label']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'single_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'music.track': {
            'Meta': {'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'to': u"orm['music.Album']"}),
            'arrangers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'arranged'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'composed'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_alternate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lyricists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wrote'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'lyrics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_alternate': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'original_track': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['music.Track']"}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'romanized_lyrics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'romanized_name_alternate': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'single': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'to': u"orm['music.Single']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'translated_lyrics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'translated_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'translation_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'})
        },
        u'music.trackorder': {
            'Meta': {'ordering': "('disc', 'position')", 'object_name': 'TrackOrder'},
            'disc': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': u"orm['music.Edition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_album_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_aside': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_bside': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_instrumental': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appears_on'", 'to': u"orm['music.Track']"})
        },
        u'music.video': {
            'Meta': {'object_name': 'Video'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videos'", 'null': 'True', 'to': u"orm['music.Album']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'single': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videos'", 'null': 'True', 'to': u"orm['music.Single']"}),
            'still': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'music.videotrackorder': {
            'Meta': {'ordering': "('position',)", 'unique_together': "(('edition', 'video'),)", 'object_name': 'VideoTrackOrder'},
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_order'", 'to': u"orm['music.Edition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'on_edition'", 'to': u"orm['music.Video']"})
        },
        u'people.group': {
            'Meta': {'ordering': "('started',)", 'object_name': 'Group'},
            'classification': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'former_names': ('ohashi.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'supergroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'through': u"orm['people.Membership']", 'to': u"orm['people.Idol']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'max_length': '60'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subgroups'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '60'}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'people.idol': {
            'Meta': {'ordering': "('birthdate',)", 'object_name': 'Idol'},
            'alias': ('ohashi.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'birthdate': ('ohashi.db.models.fields.birthdays.BirthdayField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'birthdate_dayofyear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True'}),
            'birthplace': ('ohashi.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'birthplace_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_romanized': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'bloodtype': ('ohashi.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '2', 'blank': 'True'}),
            'color': ('ohashi.db.models.fields.CharField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'idols_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'graduated': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'max_length': '60'}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'primary_membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary'", 'null': 'True', 'to': u"orm['people.Membership']"}),
            'retired': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '60'}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'idol_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'people.membership': {
            'Meta': {'ordering': "('-is_primary', '-started', '-idol__birthdate')", 'unique_together': "(('idol', 'group'),)", 'object_name': 'Membership'},
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'generation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'group': ('ohashi.db.models.fields.CustomManagerForeignKey', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['people.Idol']"}),
            'is_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'leadership_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leadership_started': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'})
        },
        u'people.staff': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Staff'},
            'alias': ('ohashi.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'staffs_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'max_length': '60'}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'staff_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        }
    }

    complete_apps = ['music']