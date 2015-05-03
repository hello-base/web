from uuid import UUID

from apps.merchandise.utils import uuid_encode


def test_encoding():
    u = UUID('{12345678-1234-5678-1234-567812345678}')
    assert uuid_encode(u) == 'VoVuUtBhZ6TvQSAYEqNdF5'
