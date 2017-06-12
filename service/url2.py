import json

from flask import Flask, request, Response
import os
import logging
import ftplib
import io

from service import xmlconverter

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
@app.route("/ftp://<host>/<path:filename>", methods=["GET"])
@app.route("/ftp://<host>:<int:port>/<path:filename>", methods=["GET"])
def get(host,filename, port=21):
    filetype = filename.split(".")
    try:
        ftp = ftplib.FTP()
        ftp.connect(host=host,port=port)
        logger.info("Logging into %s", host)
        ftp.login( os.environ.get('username'), os.environ.get('password'))

        bio = io.BytesIO()
        def handle_binary(more_data):
            bio.write(more_data)

        ftp.retrbinary("RETR "+  filename, callback=handle_binary)
        logger.info("Fetching binary from path %s", filename)
        bio.seek(0)  # Go back to the start

        logger.info("closing connection to %s", host)
        ftp.quit()

        logger.info("Filetype is %s - using %s parser", filetype[-1], filetype[-1])
        json_obj = None
        if  filetype[-1] == "xml": #add more filetypes when parsers are made
            json_obj = xmlconverter.xml_to_json(bio)
        ##TODO Add more filetypes when parsers are made
        else:
            logger.info("Filetype %s not supported", filetype[-1])
            return Response(response="Not supported filetype", status=550, mimetype='application/json')

        return Response(response=json_obj, mimetype='application/json')

    except ftplib.all_errors as e:
        logger.info('Unable to connect!,%s' % e)
        return Response(response=str(e), status=500, mimetype='application/json')

#FTP POST ROUTE
@app.route("/ftp://<host>/<path:filename>", methods=["POST"])
@app.route("/ftp://<host>:<int:port>/<path:filename>", methods=["POST"])
def post(username,password,host,filename, port=21):
    entities = request.get_json()
    filetype = filename.split(".")
    try:
        ftp = ftplib.FTP()
        ftp.connect(host=host, port=port)
        logger.info("Logging into %s", host)
        ftp.login(os.environ.get('username'), os.environ.get('password'))

        logger.info("Filetype to save is %s - using %s parser", filetype[-1], filetype[-1])
        if filetype[-1] == "xml":  # add more filetypes when parsers are made
            xml = xmlconverter.json_to_xml(entities)
            bio = io.BytesIO(xml.encode())
            bio.seek(0)
            ftp.storbinary('STOR ' + filename, bio)  # send the file
        ##TODO Add more filetypes when parsers are made
        else:
            logger.info("Filetype %s not supported", filetype[-1])
            return Response(response="Not supported filetype", status=550, mimetype='application/json')


        logger.info("closing connection to %s", host)
        ftp.quit()

        return Response(response="Great Success!", mimetype='application/json')

    except ftplib.all_errors as e:
        logger.error('Unable to connect!,%s' % e)
        return Response(response=str(e), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('port',5000))
