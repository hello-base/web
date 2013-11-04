from rest_framework import generics

from components.people.models import Membership, Group, Idol

from .serializers import (GroupSerializer, GroupMembershipSerializer,
    IdolSerializer, IdolMembershipSerializer)


class GroupMixin(object):
    model = Group
    serializer_class = GroupSerializer


class GroupList(GroupMixin, generics.ListAPIView):
    pass


class GroupDetail(GroupMixin, generics.RetrieveAPIView):
    lookup_field = 'slug'


class GroupMembershipsList(GroupMixin, generics.ListAPIView):
    serializer_class = IdolMembershipSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        memberships = Membership.objects.filter(group__slug=slug)
        return memberships


class GroupActiveMembershipsList(GroupMembershipsList):
    def get_queryset(self):
        return super(GroupActiveMembershipsList, self).get_queryset().filter(memberships__ended__isnull=True)


class GroupInactiveMembershipsList(GroupMembershipsList):
    def get_queryset(self):
        return super(GroupInactiveMembershipsList, self).get_queryset().filter(memberships__ended__isnull=False)


class IdolList(generics.ListAPIView):
    model = Idol
    serializer_class = IdolSerializer


class IdolDetail(generics.RetrieveAPIView):
    model = Idol
    serializer_class = IdolSerializer
    lookup_field = 'slug'
