from celery.decorators import task
from dateutil import parser

from .models import Channel, Video, Thumbnail


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


@task
def fetch_video(instance):
    # Connect to API and get the details.
    entry = instance.entry()

    # Set the details.
    instance.title = entry.media.title.text
    instance.description = entry.media.description.text
    instance.published = parser.parse(entry.published.text)
    instance.duration = entry.media.duration.seconds
    instance.flash_url = entry.GetSwfUrl()
    instance.watch_url = entry.media.player.url

    # Save the thumbnails.
    for thumbnail in entry.media.thumbnail:
        t = Thumbnail()
        t.url = thumbnail.url
        t.video = instance
        t.save()
