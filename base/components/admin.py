from django.contrib import admin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse


# Adds support for allowing Hello! Base ID-based authentication for
# the administration system (django.contrib.admin).
def _hello_base_id_login(self, request, **kwargs):
    if request.user.is_authenticated():
        if not request.user.is_active or not request.user.is_staff:
            raise PermissionDenied()
    else:
        return redirect_to_login(request.get_full_path(), reverse('signin'))

# Overide the standard AdminSite login form.
admin.sites.AdminSite.login = _hello_base_id_login

# Unregister Celery's administration modules.
from djcelery.models import TaskState, WorkerState, PeriodicTask, IntervalSchedule, CrontabSchedule

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
