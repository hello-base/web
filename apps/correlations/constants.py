from apps.merchandise.music.models import Album, Single
from apps.people.models import Group, Membership, Idol

SUBJECTS = [
    # Positive dates.
    (Idol, 'birthdate'),
    (Idol, 'started'), (Group, 'started'), (Membership, 'started'),
    (Membership, 'leadership_started'),
    (Album, 'released'), (Single, 'released'),

    # Negative dates.
    (Idol, 'graduated'),
    (Idol, 'retired'),
    (Group, 'ended'), (Membership, 'ended'),
    (Membership, 'leadership_ended'),
]
MODELS = set(s[0] for s in SUBJECTS)
FIELDS = set(s[1] for s in SUBJECTS)

FIELD_MAPPING = {
    ('music', 'album', 'released'): 'new albums',
    ('music', 'single', 'released'): 'new singles',
    ('people', 'group', 'ended'): 'disbanded groups',
    ('people', 'group', 'started'): 'new groups',
    ('people', 'idol', 'birthdate'): 'born',
    ('people', 'idol', 'graduated'): 'graduations',
    ('people', 'idol', 'retired'): 'retirements',
    ('people', 'idol', 'started'): 'new idols',
    ('people', 'membership', 'ended'): 'left groups',
    ('people', 'membership', 'leadership_ended'): 'new leaders',
    ('people', 'membership', 'leadership_started'): 'ex-leaders',
    ('people', 'membership', 'started'): 'joined groups',
}
