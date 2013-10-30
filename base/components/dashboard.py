from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        # Hello! Base core modules.
        self.children.append(modules.ModelList(
            title='Idols & Staff', column=1, collapsible=False,
            models=('components.people.*',),
        ))
        self.children.append(modules.ModelList(
            title='Events', column=1, collapsible=False,
            models=('components.events.*',),
        ))
        self.children.append(modules.AppList(
            title='Merchandise', column=1, collapsible=False,
            models=('components.merchandise.*',),
        ))
        self.children.append(modules.AppList(
            title='Music', column=1, collapsible=False,
            models=(
                'components.merchandise.music.models.Album',
                'components.merchandise.music.models.Single',
                'components.merchandise.music.models.Editions',
                'components.merchandise.music.models.Labels',
                'components.merchandise.music.models.Tracks',
                'components.merchandise.music.models.Videos',
            ),
        ))

        # Recent actions.
        self.children.append(modules.RecentActions(
            title='Recent Actions',
            collapsible=False,
            column=2,
            limit=10,
        ))

        # Management modules.
        self.children.append(modules.AppList(
            title='Management', column=3, collapsible=False,
            models=('components.accounts.*', 'django.contrib.*', 'djcelery.*'),
        ))
