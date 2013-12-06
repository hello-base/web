from components.merchandise.music.models import Album, Single
from components.people.models import Group, Membership, Idol

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
