from celery.decorators import task

from .models import Channel, Video


@task
def fetch_all_videos(instance):
    # Connect to the API and grab the feed.
    entries = instance.entries()
    for video in entries:
        # YouTube IDs will stay at 11 characters for the distant
        # future, so this should be a safe way to grab the ID.
        ytid = video.id.text[-11:]
        obj, created = Video.objects.get_or_create(channel=instance, ytid=ytid)
        obj.save()


@task
def fetch_latest_videos():
    for instance in Channel.objects.all():
        # Connect to the API and grab the feed.
        entries = instance.latest_entries()
        for video in entries.entry:
            # YouTube IDs will stay at 11 characters for the distant
            # future, so this should be a safe way to grab the ID.
            ytid = video.id.text[-11:]
            obj, created = Video.objects.get_or_create(channel=instance, ytid=ytid)
            obj.save()