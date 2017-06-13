import xmltodict
import json
import os

def xml_to_json(bytes, xml_path):
    root_element = xmltodict.parse(bytes)
    element = list(xml_iterator(xml_path,root_element))
    return (element)

def xml_iterator(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in xml_iterator(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in xml_iterator(key, d):
                    yield result
