# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Videodisc'
        db.create_table(u'media_videodisc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('submitted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='videodisc_submissions', null=True, to=orm['accounts.Editor'])),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('released', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1, 1, 1, 0, 0), null=True, db_index=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')(auto_add=True)),
            ('kind', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['Videodisc'])

        # Adding M2M table for field edited_by on 'Videodisc'
        m2m_table_name = db.shorten_name(u'media_videodisc_edited_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videodisc', models.ForeignKey(orm[u'media.videodisc'], null=False)),
            ('editor', models.ForeignKey(orm[u'accounts.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videodisc_id', 'editor_id'])

        # Adding M2M table for field idols on 'Videodisc'
        m2m_table_name = db.shorten_name(u'media_videodisc_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videodisc', models.ForeignKey(orm[u'media.videodisc'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videodisc_id', 'idol_id'])

        # Adding M2M table for field groups on 'Videodisc'
        m2m_table_name = db.shorten_name(u'media_videodisc_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videodisc', models.ForeignKey(orm[u'media.videodisc'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videodisc_id', 'group_id'])

        # Adding M2M table for field participating_idols on 'Videodisc'
        m2m_table_name = db.shorten_name(u'media_videodisc_participating_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videodisc', models.ForeignKey(orm[u'media.videodisc'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videodisc_id', 'idol_id'])

        # Adding M2M table for field participating_groups on 'Videodisc'
        m2m_table_name = db.shorten_name(u'media_videodisc_participating_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videodisc', models.ForeignKey(orm[u'media.videodisc'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videodisc_id', 'group_id'])

        # Adding model 'VideodiscFormat'
        db.create_table(u'media_videodiscformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='formats', null=True, to=orm['media.Videodisc'])),
            ('kind', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('released', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1, 1, 1, 0, 0), null=True, db_index=True, blank=True)),
            ('catalog_number', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('art', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['VideodiscFormat'])

        # Adding model 'Clip'
        db.create_table(u'media_clip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('kanji', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['media.VideodiscFormat'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='on_formats', null=True, to=orm['music.Track'])),
            ('disc', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'media', ['Clip'])

        # Adding unique constraint on 'Clip', fields ['format', 'track']
        db.create_unique(u'media_clip', ['format_id', 'track_id'])

        # Adding M2M table for field idols on 'Clip'
        m2m_table_name = db.shorten_name(u'media_clip_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clip', models.ForeignKey(orm[u'media.clip'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['clip_id', 'idol_id'])

        # Adding M2M table for field groups on 'Clip'
        m2m_table_name = db.shorten_name(u'media_clip_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clip', models.ForeignKey(orm[u'media.clip'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['clip_id', 'group_id'])

        # Adding M2M table for field participating_idols on 'Clip'
        m2m_table_name = db.shorten_name(u'media_clip_participating_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clip', models.ForeignKey(orm[u'media.clip'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['clip_id', 'idol_id'])

        # Adding M2M table for field participating_groups on 'Clip'
        m2m_table_name = db.shorten_name(u'media_clip_participating_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clip', models.ForeignKey(orm[u'media.clip'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['clip_id', 'group_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Clip', fields ['format', 'track']
        db.delete_unique(u'media_clip', ['format_id', 'track_id'])

        # Deleting model 'Videodisc'
        db.delete_table(u'media_videodisc')

        # Removing M2M table for field edited_by on 'Videodisc'
        db.delete_table(db.shorten_name(u'media_videodisc_edited_by'))

        # Removing M2M table for field idols on 'Videodisc'
        db.delete_table(db.shorten_name(u'media_videodisc_idols'))

        # Removing M2M table for field groups on 'Videodisc'
        db.delete_table(db.shorten_name(u'media_videodisc_groups'))

        # Removing M2M table for field participating_idols on 'Videodisc'
        db.delete_table(db.shorten_name(u'media_videodisc_participating_idols'))

        # Removing M2M table for field participating_groups on 'Videodisc'
        db.delete_table(db.shorten_name(u'media_videodisc_participating_groups'))

        # Deleting model 'VideodiscFormat'
        db.delete_table(u'media_videodiscformat')

        # Deleting model 'Clip'
        db.delete_table(u'media_clip')

        # Removing M2M table for field idols on 'Clip'
        db.delete_table(db.shorten_name(u'media_clip_idols'))

        # Removing M2M table for field groups on 'Clip'
        db.delete_table(db.shorten_name(u'media_clip_groups'))

        # Removing M2M table for field participating_idols on 'Clip'
        db.delete_table(db.shorten_name(u'media_clip_participating_idols'))

        # Removing M2M table for field participating_groups on 'Clip'
        db.delete_table(db.shorten_name(u'media_clip_participating_groups'))


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 11, 0, 0)', 'blank': 'True'}),
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
            'Meta': {'ordering': "('format', 'disc', 'position')", 'unique_together': "(('format', 'track'),)", 'object_name': 'Clip'},
            'disc': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': u"orm['media.VideodiscFormat']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'kanji': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clips_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
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