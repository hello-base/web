from django import template
register = template.Library()

from ..models import Base


@register.inclusion_tag('people/idols/idol_contexted_participants.html')
def contextual_participants(release, idol):
    groups = idol.groups.all()
    participants = release.participants
    relationships = {'solo': False, 'for': [], 'with': []}
    if len(participants) == 1:
        for participant in participants:
            if participant != idol.primary_membership.group and participant != idol:
                relationships['for'].append(participant)
            if participant == idol:
                # We return an empty dictionary to tell the template
                # tag that this is a solo work.
                relationships['solo'] = True
                return {'relationships': relationships}
    else:
        for participant in participants:
            if participant in groups:
                relationships['for'].append(participant)

                # Bait and switch, Python style. We don't want to
                # plug primary groups or idols themselves into the
                # dictionary, so we have to go back on our word
                # and remove them from it.
                if participant == idol.primary_membership.group or participant == idol:
                    relationships['for'].remove(participant)
            elif participant != idol:
                relationships['with'].append(participant)
    return {'relationships': relationships}
