from rest_framework import serializers

from components.people.models import Group, Idol


class IdolSerializer(serializers.ModelSerializer):
    photo = serializers.Field('photo.url')
    photo_thumbnail = serializers.Field('photo_thumbnail.url')

    class Meta:
        model = Idol


class GroupSerializer(serializers.ModelSerializer):
    photo = serializers.Field('photo.url')
    photo_thumbnail = serializers.Field('photo_thumbnail.url')

    class Meta:
        model = Group
