from rest_framework import serializers

from components.people.models import Group, Idol


class IdolSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('photo_url')
    photo_thumbnail = serializers.SerializerMethodField('photo_thumbnail_url')

    class Meta:
        model = Idol
        fields = ('id', 'name', 'family_name', 'given_name', 'romanized_name',
            'romanized_family_name', 'romanized_given_name', 'alias',
            'romanized_alias', 'nicknames', 'photo', 'photo_thumbnail', 'slug',
            'birthdate', 'birthdate_dayofyear', 'bloodtype', 'height',
            'primary_membership', 'status', 'scope', 'note')

    def photo_url(self, obj):
        return obj.photo.url if obj.photo else ''

    def photo_thumbnail_url(self, obj):
        return obj.photo_thumbnail.url if obj.photo_thumbnail else ''


class GroupSerializer(serializers.ModelSerializer):
    members_active = serializers.HyperlinkedIdentityField(view_name='api:group-members-active')
    photo = serializers.SerializerMethodField('photo_url')
    photo_thumbnail = serializers.SerializerMethodField('photo_thumbnail_url')

    class Meta:
        model = Group
        fields = ('id', 'name', 'romanized_name', 'former_names', 'slug',
            'started', 'ended', 'photo', 'photo_thumbnail', 'parent', 'groups',
            'members_active', 'note')

    def photo_url(self, obj):
        return obj.photo.url if obj.photo else ''

    def photo_thumbnail_url(self, obj):
        return obj.photo_thumbnail.url if obj.photo_thumbnail else ''
