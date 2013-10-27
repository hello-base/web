from django import template
register = template.Library()


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
    relationships = {'for': []}
    if participant != idol and participant != idol.primary_membership.group:
        relationships['for'].append(participant)
    if participant == idol:
        # We return an empty dictionary to tell the template
        # tag that this is a solo work.
        relationships['solo'] = True

        # Hackity hack. We DO NOT want to show the "solo work"
        # pill for memebers of the soloist group.
        if 'Soloist' in str(idol.primary_membership):
            relationships['soloist'] = True
    return relationships


def parse_idols(participants, idol):
    groups = idol.groups.all()
    relationships = {'for': [], 'with': []}
    for participant in participants:
        if participant in groups and (
            participant != idol.primary_membership.group
            or participant != idol):
            relationships['for'].append(participant)
        elif participant != idol:
            relationships['with'].append(participant)
    return relationships


def parse_groups(participants, group):
    from components.people.constants import CLASSIFICATIONS

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
