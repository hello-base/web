# -*- coding: utf-8 -*-
def call_attributes(instance, attribute_list):
    for attribute in attribute_list:
        if hasattr(instance, attribute):
            return (getattr(instance, attribute), attribute)
    raise AttributeError
