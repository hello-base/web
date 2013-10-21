from rest_framework import generics

from components.people.models import Group, Idol

from .serializers import GroupSerializer, IdolSerializer


class GroupList(generics.ListAPIView):
    model = Group
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveAPIView):
    model = Group
    serializer_class = GroupSerializer
    lookup_field = 'slug'


class IdolList(generics.ListAPIView):
    model = Idol
    serializer_class = IdolSerializer


class IdolDetail(generics.RetrieveAPIView):
    model = Idol
    serializer_class = IdolSerializer
    lookup_field = 'slug'
