from model_utils import Choices

from ohashi.constants import OTHER


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
    ]),
    (OTHER, 'other', 'Other')
)

# This is a hard-coded constant because of the Hello Pro Kenshuusei, the only
# "group" classified as Hello! Project that is not a major group.
HELLO_PROJECT_GROUPS = [1, 2, 3, 52, 54]

PHOTO_SOURCES = Choices(
    (1, 'promotional', 'Promotional Photo'),
    (2, 'blog', 'Blog Photo'),
    (OTHER, 'other', 'Other')
)

SCOPE = Choices(
    (1, 'hp', 'Hello! Project'),
    (2, 'ufa', 'Up Front Agency'),
    (OTHER, 'other', 'Other')
)

STATUS = Choices(
    (1, 'active', 'Active'),
    (2, 'former', 'Former'),
    (OTHER, 'other', 'Other')
)
