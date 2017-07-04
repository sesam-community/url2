from dotdictify import Dotdictify
import logger

logger = logger.Logger('json')

class JsonParser:
    def __init__(self, args):
        self.entities_path = args.get("entities_path")
        self._updated_path = args.get("updated_path")
        self._since = args.get("since")

    def parse(self, stream):
        return self._rest_entities(bytes=stream)

    def _rest_entities(self, bytes):
        root_element = bytes

        if self.entities_path is not None:
            l = list(Dotdictify(root_element).get(self.entities_path))
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

