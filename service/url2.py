import json

from flask import Flask, request, Response
import os
import logger
from ftp import Ftp
from ssh import Ssh
from json_parser import Json
from json_tools import JsonParser
from xml_tools import XmlParser, XmlRenderer
from csv_tools import CsvParser, CsvRenderer
app = Flask(__name__)

logger = logger.Logger('url2-service')


def create_protocol():
    protocol = os.environ.get("protocol")
    logger.info("Using protocol: %s" % protocol)
    if protocol.lower() == "ftp":
        return Ftp()
    elif protocol.lower() == "ssh":
        return Ssh()
    elif protocol.lower() == "json":
        return Json()
    else:
        raise Exception("Unknown protocol: '%s'" % protocol)


def create_parser(args, path):
    filetype = path.split(".")[-1]
    #TODO Could also use mimetype on incoming stream
    parser = args.get('type', filetype)
    logger.info("Using parser: %s" % parser)
    if parser.lower() == "xml":
        return XmlParser(args)
    elif parser.lower() == "json":
        return JsonParser(args)
    elif parser.lower() == "csv":
        return CsvParser(args)
    else:
        raise Exception("Unknown parser: '%s" % parser)


def create_renderer(args, path):
    filetype = path.split(".")[-1]

    renderer = args.get('type', filetype)
    if renderer.lower() == "xml":
        return XmlRenderer(args)
    elif renderer.lower() == "csv":
        return CsvRenderer(args)
    else:
        raise Exception("Unknown renderer: '%s" % renderer)

protocol = create_protocol()


@app.route("/<path:path>", methods=["GET"])
def get(path):
    parser = create_parser(request.args, path)
    session = protocol.open_session()
    streams = session.read(path, args=request.args)
    l = []
    for stream in streams:
        l = l + parser.parse(stream)
    session.close()
    if isinstance(parser, CsvParser):
        dumps = l
        mimetype = 'text/csv'
    else:
        dumps = json.dumps(l)
        mimetype = 'application/json'
    return Response(response=dumps, mimetype=mimetype)


@app.route('/<path:path>', methods=["POST"])
def post(path):

    renderer = create_renderer(request.args, path)
    stream = request.stream
    session = protocol.open_session()
    session.write(path, renderer.render(stream), args=request.args)
    session.close()

    return Response(response="Great Success!", mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('port',5000))
