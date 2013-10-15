# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming field 'Clip.name' to 'romanized_name'
        db.rename_column(u'media_clip', 'name', 'romanized_name')

        # Renaming field 'Clip.kanji' to 'name'
        db.rename_column(u'media_clip', 'kanji', 'name')


    def backwards(self, orm):
        # Renaming field 'Clip.name' to 'kanji'
        db.rename_column(u'media_clip', 'name', 'kanji')

        # Renaming field 'Clip.romanized_name' to 'name'
        db.rename_column(u'media_clip', 'romanized_name', 'name')


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 12, 0, 0)', 'blank': 'True'}),
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
        u'media.clip': {
            'Meta': {'ordering': "('format', 'disc', 'position')", 'object_name': 'Clip'},
            'disc': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': u"orm['media.VideodiscFormat']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'on_formats'", 'null': 'True', 'to': u"orm['music.Track']"})
        },
        u'media.videodisc': {
            'Meta': {'object_name': 'Videodisc'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'videodiscs_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'videodiscs'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'videodiscs'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'videodiscs_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'videodiscs_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videodisc_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"}),
            'uuid': ('ohashi.db.models.fields.uuids.UUIDField', [], {'auto_add': 'True'})
        },
        u'media.videodiscformat': {
            'Meta': {'ordering': "('-released',)", 'object_name': 'VideodiscFormat'},
            'art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'catalog_number': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'clips': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'videos'", 'to': u"orm['music.Track']", 'through': u"orm['media.Clip']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'formats'", 'null': 'True', 'to': u"orm['media.Videodisc']"}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'music.track': {
            'Meta': {'object_name': 'Track'},
            'arrangers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'arranged'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'composed'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'is_alternate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lyricists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wrote'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Staff']"}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'name_alternate': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'original_track': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent'", 'null': 'True', 'to': u"orm['music.Track']"}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tracks_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'romanized_name_alternate': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True', 'blank': 'True'}),
            'uuid': ('ohashi.db.models.fields.uuids.UUIDField', [], {'auto_add': 'True', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('birthdate',)", 'object_name': 'Idol'},
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

    complete_apps = ['media']
