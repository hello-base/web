# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Fact


class FactInline(admin.StackedInline):
    extra = 1
    fields = ['body']
    model = Fact
