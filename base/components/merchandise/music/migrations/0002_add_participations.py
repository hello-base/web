# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field participating_idols on 'Album'
        m2m_table_name = db.shorten_name(u'music_album_participating_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm[u'music.album'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'idol_id'])

        # Adding M2M table for field participating_groups on 'Album'
        m2m_table_name = db.shorten_name(u'music_album_participating_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm[u'music.album'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'group_id'])

        # Adding M2M table for field participating_idols on 'Single'
        m2m_table_name = db.shorten_name(u'music_single_participating_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('single', models.ForeignKey(orm[u'music.single'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['single_id', 'idol_id'])

        # Adding M2M table for field participating_groups on 'Single'
        m2m_table_name = db.shorten_name(u'music_single_participating_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('single', models.ForeignKey(orm[u'music.single'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['single_id', 'group_id'])


    def backwards(self, orm):
        # Removing M2M table for field participating_idols on 'Album'
        db.delete_table(db.shorten_name(u'music_album_participating_idols'))

        # Removing M2M table for field participating_groups on 'Album'
        db.delete_table(db.shorten_name(u'music_album_participating_groups'))

        # Removing M2M table for field participating_idols on 'Single'
        db.delete_table(db.shorten_name(u'music_single_participating_idols'))

        # Removing M2M table for field participating_groups on 'Single'
        db.delete_table(db.shorten_name(u'music_single_participating_groups'))


    models = {
        u'music.album': {
            'Meta': {'ordering': "('-released',)", 'object_name': 'Album'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_compilation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'to': u"orm['music.Label']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'number': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True', 'blank': 'True'}),
            'uuid': ('ohashi.db.models.fields.uuids.UUIDField', [], {})
        },
        u'music.edition': {
            'Meta': {'ordering': "('kind', 'romanized_name')", 'object_name': 'Edition'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'editions'", 'null': 'True', 'to': u"orm['music.Album']"}),
            'art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'catalog_number': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'single': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'editions'", 'null': 'True', 'to': u"orm['music.Single']"}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'editions'", 'to': u"orm['music.Track']", 'through': u"orm['music.TrackOrder']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'editions'", 'to': u"orm['music.Video']", 'through': u"orm['music.VideoTrackOrder']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'music.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'})
        },
        u'music.single': {
            'Meta': {'ordering': "('-released',)", 'object_name': 'Single'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'has_8cm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_cassette': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_lp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_indie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'singles'", 'null': 'True', 'to': u"orm['music.Label']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'number': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'singles_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True', 'blank': 'True'}),
            'uuid': ('ohashi.db.models.fields.uuids.UUIDField', [], {})
        },
        u'music.track': {
            'Meta': {'object_name': 'Track'},
            'arrangers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'arranged'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'composed'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_alternate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lyricists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wrote'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'name_alternate': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'romanized_name_alternate': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'})
        },
        u'music.trackorder': {
            'Meta': {'ordering': "('edition', 'position')", 'unique_together': "(('edition', 'track', 'is_instrumental'),)", 'object_name': 'TrackOrder'},
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': u"orm['music.Edition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_album_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_aside': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_bside': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_instrumental': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appears_on'", 'to': u"orm['music.Track']"})
        },
        u'music.video': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Video'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videos'", 'null': 'True', 'to': u"orm['music.Album']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'single': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videos'", 'null': 'True', 'to': u"orm['music.Single']"}),
            'still': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_url': ('ohashi.db.models.fields.URLField', [], {'blank': 'True'})
        },
        u'music.videotrackorder': {
            'Meta': {'ordering': "('edition', 'position')", 'unique_together': "(('edition', 'video'),)", 'object_name': 'VideoTrackOrder'},
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_order'", 'to': u"orm['music.Edition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'on_edition'", 'to': u"orm['music.Video']"})
        },
        u'people.group': {
            'Meta': {'object_name': 'Group'},
            'classification': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'former_names': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_groups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'has_discussions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'through': u"orm['people.Membership']", 'to': u"orm['people.Idol']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'note_processed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subgroups'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'people.idol': {
            'Meta': {'object_name': 'Idol'},
            'alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'birthdate': ('ohashi.db.models.fields.birthdays.BirthdayField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'birthdate_dayofyear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True'}),
            'birthplace': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'birthplace_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_romanized': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'bloodtype': ('ohashi.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '2', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'has_discussions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'note_processed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'primary_membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary'", 'null': 'True', 'to': u"orm['people.Membership']"}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'people.membership': {
            'Meta': {'ordering': "('-is_primary', '-started', '-idol__birthdate')", 'unique_together': "(('idol', 'group'),)", 'object_name': 'Membership'},
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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
            'alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['music']