from rest_framework import serializers

from components.people.models import Group, Idol, Membership


class IdolSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('photo_url')
    photo_thumbnail = serializers.SerializerMethodField('photo_thumbnail_url')
    status = serializers.CharField(source='get_status_display')
    scope = serializers.CharField(source='get_scope_display')

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
    groups = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:group-detail')
    members = serializers.HyperlinkedIdentityField(view_name='api:group-members')
    members_active = serializers.HyperlinkedIdentityField(view_name='api:group-members-active')
    members_inactive = serializers.HyperlinkedIdentityField(view_name='api:group-members-inactive')
    parent = serializers.HyperlinkedRelatedField(view_name='api:group-detail')
    photo = serializers.SerializerMethodField('photo_url')
    photo_thumbnail = serializers.SerializerMethodField('photo_thumbnail_url')

    class Meta:
        model = Group
        fields = ('id', 'name', 'romanized_name', 'former_names', 'slug',
            'started', 'ended', 'photo', 'photo_thumbnail', 'parent', 'groups',
            'members', 'members_active', 'members_inactive', 'note')

    def photo_url(self, obj):
        return obj.photo.url if obj.photo else ''

    def photo_thumbnail_url(self, obj):
        return obj.photo_thumbnail.url if obj.photo_thumbnail else ''


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership


class IdolMembershipSerializer(MembershipSerializer):
    idol = IdolSerializer()

    class Meta:
        model = Membership
        fields = ('id', 'idol', 'is_primary', 'started', 'ended', 'generation',
            'is_leader', 'leadership_started', 'leadership_ended')


class GroupMembershipSerializer(MembershipSerializer):
    group = GroupSerializer()

    class Meta:
        model = Membership
        fields = ('id', 'group', 'is_primary', 'started', 'ended', 'generation',
            'is_leader', 'leadership_started', 'leadership_ended')
