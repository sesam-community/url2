import json

from flask import Flask, request, Response
import os
import logging
from service import xml, ftptools

app = Flask(__name__)

logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('url2-service')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

#FTP GET ROUTE
@app.route("/<path:path>", methods=["GET"])
def get(path):
    request_method = request.method
    json_obj = protocol(request_method, path, args=request.args)
    if json_obj == "null":
        return Response(response=None, status=400, mimetype='application/json')
    else:
        return Response(response=json_obj, mimetype='application/json')

#FTP POST ROUTE
@app.route('/<path:path>', methods=["POST"])
def post(path):
    request_method = request.method
    renderer(request_method,path,request.stream.read())

    return Response(response="Great Success!", mimetype='application/json')

def renderer(request_method, path, bytes):
    filetype = path.split(".")
    if filetype[-1].lower() == "xml":
        protocol(request_method, path, bytes)
    else:
        logger.log("No renderer found for filetype %s", filetype[-1])

#TODO: add more protocols
def protocol(request_method, path, bytes=None, args=None):

    if request_method == "POST":
        if os.environ.get("protocol") == "ftp":
            connection =ftptools.ftp_connect()
            ftptools.ftp_savefile(connection, path, bytes)
            connection.quit()
    elif request_method == "GET":
        if os.environ.get('protocol') == "ftp":
            connection = ftptools.ftp_connect()
            return json.dumps(parser(ftptools.ftp_get_file(connection, path, args), args, path))
            connection.quit()
        return

#TODO: add more parsers
def parser(bio, args,path):
    parser = args.get("parser")

    bio.seek(0)
    if parser == "xml":
        logger.info("Filetype is %s - using %s parser", parser, parser)
        return xml.xml_to_json(bio, args.get("xml_path"))
    else:
        logger.info("Filetype %s not supported", parser)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('port',5000))
