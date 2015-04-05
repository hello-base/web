from rest_framework import generics

from base.apps.people.models import Membership, Group, Idol

from .serializers import (GroupSerializer, IdolSerializer,
    IdolMembershipSerializer, MembershipSerializer)


class GroupMixin(object):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupList(GroupMixin, generics.ListAPIView):
    pass


class GroupDetail(GroupMixin, generics.RetrieveAPIView):
    lookup_field = 'slug'


class GroupMembershipsList(GroupMixin, generics.ListAPIView):
    serializer_class = IdolMembershipSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        memberships = Membership.objects.order_by('started').filter(group__slug=slug)
        return memberships


class GroupActiveMembershipsList(GroupMembershipsList):
    def get_queryset(self):
        return super(GroupActiveMembershipsList, self).get_queryset().filter(ended__isnull=True)


class GroupInactiveMembershipsList(GroupMembershipsList):
    def get_queryset(self):
        return super(GroupInactiveMembershipsList, self).get_queryset().filter(ended__isnull=False)


class IdolList(generics.ListAPIView):
    queryset = Idol.objects.all()
    serializer_class = IdolSerializer


class IdolDetail(generics.RetrieveAPIView):
    queryset = Idol.objects.all()
    serializer_class = IdolSerializer
    lookup_field = 'slug'


class MembershipList(generics.ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
