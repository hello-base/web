from django import template
register = template.Library()

from apps.people.models import Group


@register.inclusion_tag('people/partials/contexted_participants.html')
def contextual_participants(release, context):
    participants = release.participants
    if context.identifier == 'idol':
        try:
            (participant,) = participants
            relationships = parse_idol(participant, context)
        except ValueError:
            relationships = parse_idols(participants, context)
    if context.identifier == 'group':
        relationships = parse_groups(participants, context)
    return {'relationships': relationships}


def parse_idol(participant, idol):
    relationships = {}
    if not isinstance(participant, Group):
        relationships['solo'] = True
        if 'Soloist' in str(idol.primary_membership):
            # Hackity hack. We DO NOT want to show the "solo work"
            # pill for memebers of the soloist group.
            relationships['soloist'] = True
    elif participant != idol.primary_membership.group:
        relationships['for'] = [participant]
    return relationships


def parse_idols(participants, idol):
    groups = idol.groups.all()
    relationships = {'for': [], 'with': []}
    for participant in participants:
        if participant in groups and participant != idol.primary_membership.group:
            relationships['for'].append(participant)
        elif participant != idol:
            relationships['with'].append(participant)
    return relationships


def parse_groups(participants, group):
    from apps.people.constants import CLASSIFICATIONS

    relationships = {'for': [], 'with': []}
    for participant in participants:
        if (hasattr(participant, 'classification')
            and participant.classification == CLASSIFICATIONS.supergroup
            or participant.id == 25) and participant != group:
            # We have a supergroup. That's all we need.
            # Also, H!P All Stars is a supergroup in my view! D:
            relationships['for'].append(participant)
            return relationships
        elif participant != group:
            relationships['with'].append(participant)
    return relationships
