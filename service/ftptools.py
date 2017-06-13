import ftplib
import os
import logging
import io
import json
import xmltodict

logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('url2-service')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

def ftp_connect():
    try:
        ftp = ftplib.FTP()
        ftp.connect(host=os.environ.get('ftp_server'), port=int(os.environ.get('ftp_port')))
        logger.info("Logging into %s", os.environ.get('ftp_server'))
        ftp.login(os.environ.get('username'), os.environ.get('password'))
        return ftp
    except ftplib.all_errors as e:
        logger.info('Unable to connect!,%s' % e)


def ftp_savefile(connection,path,stream):
    connection.storbinary('STOR ' + path,
                          io.BytesIO(xmltodict.unparse(json.loads(stream),
                            pretty=True, full_document=False).encode()))  # send the file

def ftp_get_single_file(ftp, path):
    bio = io.BytesIO()
    def handle_binary(more_data):
        bio.write(more_data)

    ftp.retrbinary("RETR " + path, callback=handle_binary)
    return bio

def ftp_input_bytes(args, ftp, path):
    delete_after = args.get('delete_after')

    bio = None
    if args.get('filename') is None:
        bio=ftp_glob(ftp,path, delete_after)
    else:
        bio=ftp_single_file(ftp, path)

    return bio

def ftp_glob(ftp,file_path, delete_after):
    ftp.cwd(file_path) #changing directory
    bio_list = []
    bio = io.BytesIO()

    def handle_binary(more_data):
        bio.write(more_data)
    try:
        files = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise

    for filename in files:
        logger.info("Fetching binary from path %s", filename)
        ftp.retrbinary("RETR " + filename, callback=handle_binary)
        bio.seek(0)  # Go back to the start
        bio_list.append(bio)
        bio = io.BytesIO() #new bytes IO

    if delete_after == "true":
        for filename in files:
            ftp.delete(filename)

    return bio_list

