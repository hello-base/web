# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class AuditListView(TemplateView):
    template_name = 'audits/audit_list.html'
