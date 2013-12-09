# -*- coding: utf-8 -*-
import datetime
import pytest

from bs4 import BeautifulSoup

from django.template import Template, Context

from components.correlations.models import Correlation
from components.people.factories import GroupFactory


