# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from markdown import Extension
from markdown.inlinepatterns import BRK, NOIMG, Pattern
from markdown.util import etree

from components.people.models import Idol

CODING_RE = r'\[([^\]]+)\]\{([^}]+)\}'


class LyricCodingExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        coding = LyricCodingPattern(CODING_RE, md)
        md.inlinePatterns.add('lyriccoding', coding, '_begin')


class LyricCodingPattern(Pattern):
    def handle_match(self, m):
        # Create a parent <span> element that'll encompass all.
        lyric = etree.Element('span')
        lyric.text = m.group(2)

        # Take the second match...
        idols = m.group(3).split(',')
        for i, idol in enumerate(idols):
            etree.SubElement(lyric, 'span')
            lyric[i].text = idol
        return lyric


def makeExtension(configs=None):
    return LyricCodingExtension(configs=configs)
