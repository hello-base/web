from ohashi.db import models

# TODO: Inherit from a custom user class of some kind.
# Maybe that should be in here? The only form of users we have on Base
# ARE editors... I think.
class Editor(models.Model):
    username = models.CharField()


class ContributorMixin(models.Model):
    submitted_by = models.ForeignKey(Editor, related_name='submissions')
    edited_by = models.ManyToManyField(Editor, related_name='edits')

    class Meta:
        abstract = True
