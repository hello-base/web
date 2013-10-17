from celery.decorators import task


@task
def render_participants(instance):
    from components.people.models import Idol, Membership

    # Do we have existing participants? Clear them out so we can
    # calculate them again.
    instance.participating_groups.clear()
    instance.participating_idols.clear()

    groups = instance.groups.all()
    if groups.exists():
        # If a supergroup is one of the groups attributed, just
        # show the supergroup.
        if instance.supergroup in groups:
            return instance.participating_groups.add(instance.supergroup)

        # Gather all of the individual idol's primary keys
        # attributed to the single into a set().
        idols = instance.idols.all()

        # Specify an empty set() that will contain all of the
        # members of the groups attributed to the single. Then,
        # loop through all of the groups and update the set with
        # all of the individual members' primary keys.
        group_ids = groups.values_list('id', flat=True)
        group_members = Membership.objects.filter(group__in=group_ids).values_list('idol', flat=True)

        # Subtract group_members from idols.
        distinct_idols = idols.exclude(pk__in=group_members)

        # Add the calculated groups and idols to our new list of
        # participating groups and idols.
        instance.participating_groups.add(*list(groups))
        instance.participating_idols.add(*list(distinct_idols))
        return

    # No groups? Just add all the idols.
    instance.participating_idols.add(*list(instance.idols.all()))
    return
