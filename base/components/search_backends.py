# -*- coding: utf-8 -*-
from haystack.backends.elasticsearch_backend import (ElasticsearchSearchBackend,
    ElasticsearchSearchEngine)


class KuromojiElasticsearchBackend(ElasticsearchSearchBackend):
    def __init__(self, connection_alias, **connection_options):
        super(KuromojiElasticsearchBackend, self).__init__(connection_alias, **connection_options)

        SETTINGS = {
            'settings': {
                'analysis': {
                    'analyzer': {
                        'ngram_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'lowercase',
                            'filter': ['haystack_ngram']
                        },
                        'edgengram_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'lowercase',
                            'filter': ['haystack_edgengram']
                        },
                        'kuromoji_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'kuromoji_tokenizer'
                        },
                    },
                    'tokenizer': {
                        'haystack_ngram_tokenizer': {
                            'type': 'nGram',
                            'min_gram': 3,
                            'max_gram': 15,
                        },
                        'haystack_edgengram_tokenizer': {
                            'type': 'edgeNGram',
                            'min_gram': 2,
                            'max_gram': 15,
                            'side': 'front',
                        },
                        'kuromoji': {
                            'type': 'kuromoji_tokenizer'
                        },
                    },
                    'filter': {
                        'haystack_ngram': {
                            'type': 'nGram',
                            'min_gram': 3,
                            'max_gram': 15,
                        },
                        'haystack_edgengram': {
                            'type': 'edgeNGram',
                            'min_gram': 5,
                            'max_gram': 15,
                        },
                        'kuromoji_rf': {
                            'type': 'kuromoji_readingform',
                            'use_romaji': 'true',
                        },
                        'kuromoji_pos': {
                            'type': 'kuromoji_part_of_speech',
                            'enable_position_increment': 'false',
                            'stoptags': ['# verb-main:', '動詞-自立']
                        },
                        'kuromoji_ks': {
                            'type': 'kuromoji_stemmer',
                            'minimum_length': 6
                        },
                    }
                }
            }
        }
        setattr(self, 'DEFAULT_SETTINGS', SETTINGS)


class KuromojiElastcisearchEngine(ElasticsearchSearchEngine):
    backend = KuromojiElasticsearchBackend
