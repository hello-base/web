from celery.decorators import task


@task
def fetch_all_videos(instance):
    # Connect to the API and grab the feed.
    videos = instance.fetch_all_videos()
    for video in videos:
        # YouTube IDs will stay at 11 characters for the distant
        # future, so this should be a safe way to grab the ID.
        ytid = video.id.text[-11:]
        obj, created = Video.objects.get_or_create(channel=instance, ytid=ytid)
        obj.save()
