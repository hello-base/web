from rest_framework import generics

from components.people.models import Group, Idol

from .serializers import GroupSerializer, IdolSerializer


class GroupList(generics.ListAPIView):
    model = Group
    serializer_class = GroupSerializer


class IdolList(generics.ListAPIView):
    model = Idol
    serializer_class = IdolSerializer
