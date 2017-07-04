import xmltodict
import json
from dotdictify import Dotdictify
import logger

logger = logger.Logger('xml')

class XmlParser:
    def __init__(self, args):
        self._xml_path = args.get("xml_path")
        self._updated_path = args.get("updated_path")
        self._since = args.get("since")

    def parse(self, stream):
        return self._xml_to_json(bytes=stream)

    def _xml_to_json(self, bytes):
        root_element = xmltodict.parse(bytes)

        if self._xml_path is not None:
            l = list(Dotdictify(root_element).get(self._xml_path))
        else:
            l = [root_element]
        if self._updated_path is not None:
            for entity in l:
                b = Dotdictify(entity)
                entity["_updated"] = b.get(self._updated_path)
        if self._since is not None:
            logger.info("Fetching data since: %s" % self._since)
            return list(filter(l, self._since))
        return l


def filter(l, since):
    for e in l:
        if e.get("_updated") > since:
            yield e


class XmlRenderer:
    def __init__(self, args):
        pass

    def render(self, stream):
        return json_to_xml(stream)


def json_to_xml(stream):
    logger.info("converting XML to json")
    return xmltodict.unparse(json.load(stream), pretty=True, full_document=False).encode()
