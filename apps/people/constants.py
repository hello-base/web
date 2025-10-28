from model_utils import Choices

from apps.ohashi.constants import OTHER


BLOOD_TYPE = Choices('A', 'B', 'O', 'AB')

CLASSIFICATIONS = Choices(
    (1, 'major', 'Major Unit'),
    (2, 'minor', 'Minor Unit'),
    (4, 'temporary', 'Temporary Unit'),
    (5, 'subunit', 'Sub-Unit'),
    (7, 'supergroup', 'Supergroup'),
    ('Special Units', [
        (3, 'shuffle', 'Shuffle Unit'),
        (6, 'revival', 'Revival Unit'),
        (8, 'satoyama', 'Satoyama Unit'),
        (9, 'satoumi', 'Satoumi Unit'),
    ]),
    (OTHER, 'other', 'Other')
)

PHOTO_SOURCES = Choices(
    (1, 'promotional', 'Promotional Photo'),
    (2, 'blog', 'Blog Photo'),
    (OTHER, 'other', 'Other')
)

SCOPE = Choices(
    (1, 'hp', 'Hello! Project'),
    ('Up-Front', [
        (11, 'ufc', 'Up-Front Create'),
        (12, 'jp', 'Just Production'),
        (13, 'jproom', 'J.P ROOM'),
    ]),
    (OTHER, 'other', 'Other')
)

STATUS = Choices(
    (1, 'active', 'Active'),
    (2, 'former', 'Former'),
    (OTHER, 'other', 'Other')
)
