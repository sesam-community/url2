import json

from flask import Flask, request, Response
import os
from service import logger
from service.ftp import Ftp
from service.ssh import Ssh
from service.xml_tools import XmlParser, XmlRenderer
app = Flask(__name__)

logger = logger.Logger('url2-service')


def create_protocol():
    protocol = os.environ.get("protocol")
    logger.info("Using protocol: %s" % protocol)
    if protocol.lower() == "ftp":
        return Ftp()
    if protocol.lower() == "ssh":
        return Ssh()
    else:
        raise Exception("Unknown protocol: '%s'" % protocol)


def create_parser(args, path):
    filetype = path.split(".")[-1]
    #TODO Could also use mimetype on incoming stream
    parser = args.get('type', filetype)
    logger.info("Using parser: %s" % parser)
    if parser.lower() == "xml":
        return XmlParser(args)
    else:
        raise Exception("Unknown parser: '%s" % parser)


def create_renderer(args, path):
    filetype = path.split(".")[-1]

    renderer = args.get('type', filetype)
    if renderer.lower() == "xml":
        return XmlRenderer(args)
    else:
        raise Exception("Unknown parser: '%s" % renderer)

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
    dumps = json.dumps(l)
    return Response(response=dumps, mimetype='application/json')


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
