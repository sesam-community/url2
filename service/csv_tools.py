import csv
import json
from dict_to_csv import transform

import logger

logger = logger.Logger("csv")
class CsvParser:
    def __init__(self, args):
        pass

    def parse(self, stream):
        return list(stream)


class CsvRenderer:
    def __init__(self, args):
        self._include_headers = (args.get("include_headers")).lower() not in ["false", "0"]
        self._keys = None
        if args.get("keys"):
            self._keys = args.get("keys").split(",")

    def render(self, stream):
        return json_to_csv(stream, self._include_headers, self._keys)


def json_to_csv(stream, include_headers, keys):
    logger.info("converting json to csv" + str(type(include_headers)))
    json_data = json.loads(stream.read().decode("utf-8"))
    csv_data = transform(json_data, include_headers, keys)
    return csv_data.encode("utf-8")
