from django import template
register = template.Library()

from components.people.constants import CLASSIFICATIONS


@register.inclusion_tag('people/partials/idol_contexted_participants.html')
def contextual_participants(release, context):
    if context.identifier == 'idol':
        return _render_idol_contextual_participants(release, context)
    if context.identifier == 'group':
        return _render_group_contextual_participants(release, context)


def _render_idol_contextual_participants(release, idol):
    groups = idol.groups.all()
    participants = release.participants
    relationships = {'solo': False, 'soloist': False, 'for': [], 'with': []}
    if len(participants) == 1:
        for participant in participants:
            if participant != idol.primary_membership.group and participant != idol:
                relationships['for'].append(participant)
            if participant == idol:
                # We return an empty dictionary to tell the template
                # tag that this is a solo work.
                relationships['solo'] = True

                # Hackity hack. We DO NOT want to show the "solo work"
                # pill for memebers of the soloist group.
                if 'Soloist' in str(idol.primary_membership):
                    relationships['soloist'] = True

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


def _render_group_contextual_participants(release, group):
    participants = release.participants
    relationships = {'for': [], 'with': []}
    for participant in participants:
        if (hasattr(participant, 'classification')
            and participant.classification == CLASSIFICATIONS.supergroup
            or participant.id == 25) and participant != group:
            # We have a supergroup. That's all we need.
            # Also, H!P All Stars is a supergroup in my view! D:
            relationships['for'].append(participant)
            return {'relationships': relationships}
        elif participant != group:
            relationships['with'].append(participant)
    return {'relationships': relationships}
