# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class AuditListView(TemplateView):
    template_name = 'audits/audit_list.html'

    def get_context_data(self, **kwargs):
        context = super(AuditListView, self).get_context_data(**kwargs)
        return context
