import collections
import redis
import time

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


def build_value(instance):
    return '%d:%d' % (ContentType.objects.get_for_model(instance).id, instance.id)


def factory_object(ct_obj_string):
    """
    Utility function that takes a content_type:object_id
    string and returns a django object.

      @ct_obj_string => '1:22'  ('content_type_id:object_id')

    """
    # Source: http://git.io/2tCSwQ
    ct_id, obj_id = ct_obj_string.split(':')
    return ContentType.objects.get_for_id(ct_id).model_class().objects.get(pk=obj_id)


def get_redis_connection():
    REDIS = settings.REDIS['default']
    credentials = {key.lower(): value for key, value in REDIS.iteritems()}
    return redis.StrictRedis(**credentials)


def construct_list_using_index(start=0, num=0, storage_key=None):
    redis = get_redis_connection()
    num = num - 1  # `num` is 0-indexed, we specify a 1-index to eliminate confusion.
    redis_results = redis.zrevrange(storage_key, start=start, num=num)

    mapping = collections.defaultdict(list)
    for x in redis_results:
        ct_id, obj_id = x.split(':')
        mapping[ct_id].append(obj_id)

    final = []
    for ct_id, obj_ids in mapping.iteritems():
        final.extend(ContentType.objects.get_for_id(ct_id).model_class().objects.filter(pk__in=obj_ids))
    return final


def construct_list_using_score(min=0, max=0, storage_key=None):
    redis = get_redis_connection()
    redis_results = redis.zrevrangebyscore(storage_key, min=0, max=0)
    return [factory_object(ct_obj_string) for ct_obj_string in redis_results]


def paginate_list(page=1, results_per_page=20, storage_key=None):
    redis = get_redis_connection()
    max_score = int(time.time())
    count = redis.zcount(storage_key, min=0, max=max_score)

    # Calculate the 'start' index.
    start = count - (results_per_page * page)
    if start < 0:
        start = 0

    # Fetch a slice of the results for the page given.
    redis_results = redis.zrangebyscore(storage_key, min=0, max=max_score, start=start, num=results_per_page)
    redis_results.reverse()
    return [factory_object(ct_obj_string) for ct_obj_string in redis_results]
