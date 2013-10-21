from rest_framework import serializers

from components.people.models import Group, Idol


class IdolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idol


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
