import os
import logger
import json
import requests
from dotdictify import Dotdictify

logger = logger.Logger("json")


class Json:
    def __init__(self):
        pass

    def open_session(self):
        return JsonRestSession()


class JsonRestSession:
    def __init__(self):
        self._connection = connect()
        logger.info("Opened connection")

    def read(self, path, args):
        return get(self._connection, path, args=args)

    def write(self, path, stream, args):
        savefile(self._connection, path, stream=stream)

    def close(self):
        logger.info("Closed connection")
        pass


def connect():
    pass


def savefile(connection, path, stream):
    connection.exec_command('echo ' + str(stream) + ' > ' + path + '\n')


def get(connection, path, args):
    streams = []
    origin_path = path
    headers = json.loads(os.environ.get('headers').replace("'", "\""))

    page_number = int(os.environ.get('page_number'))
    pages = None

    while pages is None or pages >= page_number:
        path = origin_path
        path = path.replace("page_size", os.environ.get('page_size'))
        path = path.replace("page_number", str(page_number))
        url = os.environ.get('hostname') + path
        result = Dotdictify(json.loads(requests.get(url, headers=headers).text))
        streams.append(result)

        if args.get('total_pages_path') is not None:
            pages = result.get(args.get('total_pages_path'))
        else:
            raise Exception("Missing total_pages_path")

        page_number = page_number + 1

    return streams
