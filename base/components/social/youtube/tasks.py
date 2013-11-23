from celery.decorators import task

from .api import Api
from .models import Channel, Video


def initialize_api():
    return Api()


@task
def fetch_all_videos(username):
    # Connect to the API and grab the feed.
    api = initialize_api()
    channel = Channel.objects.get(username=username)
    entries = api.get_all_videos(channel.ytid)
    for ytid in entries:
        # YouTube IDs will stay at 11 characters for the distant
        # future, so this should be a safe way to grab the ID.
        obj, created = Video.objects.get_or_create(channel=channel, ytid=ytid)
        obj.save()


@task
def fetch_latest_videos():
    for channel in Channel.objects.all():
        # Connect to the API and grab the feed.
        api = initialize_api()
        entries = api.get_latest_videos(channel.ytid)
        for ytid in entries:
            # YouTube IDs will stay at 11 characters for the distant
            # future, so this should be a safe way to grab the ID.
            obj, created = Video.objects.get_or_create(channel=channel, ytid=ytid)
            obj.save()
