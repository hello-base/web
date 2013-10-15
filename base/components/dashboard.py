from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # Hello! Base core modules.
        self.children.append(modules.Group(
            title='Hello! Base', column=1, collapsible=False,
            children=[
                modules.ModelList(
                    title='Idols & Staff', column=1, collapsible=False,
                    models=('components.people.*',),
                ),
                modules.ModelList(
                    title='Media', column=1, collapsible=False,
                    models=('components.merchandise.media.*',),
                ),
                modules.ModelList(
                    title='Goods', column=1, collapsible=False,
                    models=('components.merchandise.goods.*',),
                ),
                modules.ModelList(
                    title='Music', column=1, collapsible=False,
                    models=('components.merchandise.music.*',),
                ),
            ]
        ))

        # Management modules.
        self.children.append(modules.AppList(
            title='Management', column=2, collapsible=False,
            models=('components.accounts.*', 'django.contrib.*',),
        ))

        # Recent actions.
        self.children.append(modules.RecentActions(
            title='Recent Actions',
            collapsible=False,
            column=3,
            limit=10,
        ))
