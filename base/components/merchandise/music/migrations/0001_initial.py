# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Label'
        db.create_table(u'music_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True)),
        ))
        db.send_create_signal(u'music', ['Label'])

        # Adding model 'Album'
        db.create_table(u'music_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('released', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1, 1, 1, 0, 0), null=True, db_index=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')()),
            ('number', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='albums', null=True, to=orm['music.Label'])),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True, blank=True)),
            ('is_compilation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'music', ['Album'])

        # Adding M2M table for field idols on 'Album'
        m2m_table_name = db.shorten_name(u'music_album_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm[u'music.album'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'idol_id'])

        # Adding M2M table for field groups on 'Album'
        m2m_table_name = db.shorten_name(u'music_album_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm[u'music.album'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'group_id'])

        # Adding model 'Single'
        db.create_table(u'music_single', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('released', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1, 1, 1, 0, 0), null=True, db_index=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')()),
            ('number', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='singles', null=True, to=orm['music.Label'])),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True, blank=True)),
            ('is_indie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_8cm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_lp', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_cassette', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'music', ['Single'])

        # Adding M2M table for field idols on 'Single'
        m2m_table_name = db.shorten_name(u'music_single_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('single', models.ForeignKey(orm[u'music.single'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['single_id', 'idol_id'])

        # Adding M2M table for field groups on 'Single'
        m2m_table_name = db.shorten_name(u'music_single_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('single', models.ForeignKey(orm[u'music.single'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['single_id', 'group_id'])

        # Adding model 'Edition'
        db.create_table(u'music_edition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='editions', null=True, to=orm['music.Album'])),
            ('single', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='editions', null=True, to=orm['music.Single'])),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('kind', self.gf('django.db.models.fields.IntegerField')(default=1, db_index=True)),
            ('released', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('catalog_number', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('art', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'music', ['Edition'])

        # Adding model 'Track'
        db.create_table(u'music_track', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('is_cover', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_alternate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('romanized_name_alternate', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('name_alternate', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
        ))
        db.send_create_signal(u'music', ['Track'])

        # Adding M2M table for field idols on 'Track'
        m2m_table_name = db.shorten_name(u'music_track_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm[u'music.track'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['track_id', 'idol_id'])

        # Adding M2M table for field groups on 'Track'
        m2m_table_name = db.shorten_name(u'music_track_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm[u'music.track'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['track_id', 'group_id'])

        # Adding M2M table for field arrangers on 'Track'
        m2m_table_name = db.shorten_name(u'music_track_arrangers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm[u'music.track'], null=False)),
            ('staff', models.ForeignKey(orm[u'people.staff'], null=False))
        ))
        db.create_unique(m2m_table_name, ['track_id', 'staff_id'])

        # Adding M2M table for field composers on 'Track'
        m2m_table_name = db.shorten_name(u'music_track_composers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm[u'music.track'], null=False)),
            ('staff', models.ForeignKey(orm[u'people.staff'], null=False))
        ))
        db.create_unique(m2m_table_name, ['track_id', 'staff_id'])

        # Adding M2M table for field lyricists on 'Track'
        m2m_table_name = db.shorten_name(u'music_track_lyricists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm[u'music.track'], null=False)),
            ('staff', models.ForeignKey(orm[u'people.staff'], null=False))
        ))
        db.create_unique(m2m_table_name, ['track_id', 'staff_id'])

        # Adding model 'TrackOrder'
        db.create_table(u'music_trackorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['music.Edition'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appears_on', to=orm['music.Track'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('is_aside', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_bside', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_album_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_instrumental', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'music', ['TrackOrder'])

        # Adding unique constraint on 'TrackOrder', fields ['edition', 'track', 'is_instrumental']
        db.create_unique(u'music_trackorder', ['edition_id', 'track_id', 'is_instrumental'])

        # Adding model 'Video'
        db.create_table(u'music_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='videos', null=True, to=orm['music.Album'])),
            ('single', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='videos', null=True, to=orm['music.Single'])),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('kind', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('released', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('still', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('video_url', self.gf('ohashi.db.models.fields.URLField')(blank=True)),
        ))
        db.send_create_signal(u'music', ['Video'])

        # Adding model 'VideoTrackOrder'
        db.create_table(u'music_videotrackorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video_order', to=orm['music.Edition'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='on_edition', to=orm['music.Video'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'music', ['VideoTrackOrder'])

        # Adding unique constraint on 'VideoTrackOrder', fields ['edition', 'video']
        db.create_unique(u'music_videotrackorder', ['edition_id', 'video_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'VideoTrackOrder', fields ['edition', 'video']
        db.delete_unique(u'music_videotrackorder', ['edition_id', 'video_id'])

        # Removing unique constraint on 'TrackOrder', fields ['edition', 'track', 'is_instrumental']
        db.delete_unique(u'music_trackorder', ['edition_id', 'track_id', 'is_instrumental'])

        # Deleting model 'Label'
        db.delete_table(u'music_label')

        # Deleting model 'Album'
        db.delete_table(u'music_album')

        # Removing M2M table for field idols on 'Album'
        db.delete_table(db.shorten_name(u'music_album_idols'))

        # Removing M2M table for field groups on 'Album'
        db.delete_table(db.shorten_name(u'music_album_groups'))

        # Deleting model 'Single'
        db.delete_table(u'music_single')

        # Removing M2M table for field idols on 'Single'
        db.delete_table(db.shorten_name(u'music_single_idols'))

        # Removing M2M table for field groups on 'Single'
        db.delete_table(db.shorten_name(u'music_single_groups'))

        # Deleting model 'Edition'
        db.delete_table(u'music_edition')

        # Deleting model 'Track'
        db.delete_table(u'music_track')

        # Removing M2M table for field idols on 'Track'
        db.delete_table(db.shorten_name(u'music_track_idols'))

        # Removing M2M table for field groups on 'Track'
        db.delete_table(db.shorten_name(u'music_track_groups'))

        # Removing M2M table for field arrangers on 'Track'
        db.delete_table(db.shorten_name(u'music_track_arrangers'))

        # Removing M2M table for field composers on 'Track'
        db.delete_table(db.shorten_name(u'music_track_composers'))

        # Removing M2M table for field lyricists on 'Track'
        db.delete_table(db.shorten_name(u'music_track_lyricists'))

        # Deleting model 'TrackOrder'
        db.delete_table(u'music_trackorder')

        # Deleting model 'Video'
        db.delete_table(u'music_video')

        # Deleting model 'VideoTrackOrder'
        db.delete_table(u'music_videotrackorder')


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