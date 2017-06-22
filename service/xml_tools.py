import xmltodict
import json


class XmlParser:
    def __init__(self, args):
        self._xml_path = args.get("xml_path")

    def parse(self, stream):
        return xml_to_json(bytes=stream, xml_path=self._xml_path)


class XmlRenderer:
    def __init__(self, args):
        pass

    def render(self, stream):
        return json_to_xml(stream)


def xml_to_json(bytes, xml_path):
    root_element = xmltodict.parse(bytes)
    if xml_path is not None:
        return list(xml_iterator(xml_path,root_element))
    return [root_element]


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


def json_to_xml(stream):
    return xmltodict.unparse(json.loads(stream), pretty=True, full_document=False).encode()
