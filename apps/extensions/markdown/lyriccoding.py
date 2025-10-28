# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.urls import reverse

from markdown import Extension
from markdown.inlinepatterns import BRK, NOIMG, Pattern
from markdown.util import etree

from apps.people.models import Idol

re_coding = r'\[([^\]]+)\]\{([^}]+)\}'
re_name = re.compile('@([a-zA-Z+_-]+)')


class LyricCodingExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        coding = LyricCodingPattern(re_coding, md)
        md.inlinePatterns.add('lyriccoding', coding, '_begin')


class LyricCodingPattern(Pattern):
    def handleIdol(self, element, idol):
        # Fetch the idol.
        match = re_name.search(idol)
        idol = Idol.objects.get(slug=match.group(1))

        # Build the containing <span>, then create one sub-element to provide
        # a  link to the idol and another sub-element that will house the
        # idol's image.
        element.attrib['class'] = 'lyric-idol idol-%s' % (match.group(1))
        element.attrib['href'] = reverse('idol-detail', kwargs={'slug': match.group(1)})
        etree.SubElement(element, 'img')
        element[0].attrib['class'] = 'lyric-idol-img'
        element[0].attrib['src'] = idol.optimized_square.url
        element[0].attrib['title'] = idol.romanized_name
        return element

    def handleMatch(self, match):
        # Create a parent <span> element that'll encompass all.
        lyric = etree.Element('span')
        lyric.attrib['class'] = 'lyric-line'
        lyric.text = match.group(2)

        # Take the second match...
        etree.SubElement(lyric, 'span')
        wrapper = lyric[0]
        wrapper.attrib['class'] = 'lyric-idols'
        idols = match.group(3).split(',')
        for i, idol in enumerate(idols):
            etree.SubElement(wrapper, 'a')
            wrapper[i] = self.handleIdol(wrapper[i], idol)
        return lyric


def makeExtension(configs=None):
    return LyricCodingExtension(configs=configs)
