import xmltodict
import json
import os

def xml_to_json(bytes):
    root_element = xmltodict.parse(bytes)
    element = list(xml_iterator(os.environ.get('xml_path'),root_element))
    return (json.dumps(element))

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

def json_to_xml(entities):
    if not isinstance(entities, list):
        entities = [entities]
    for i in entities:
        print (i)
        xml = xmltodict.unparse(i, pretty=True)
    return xml