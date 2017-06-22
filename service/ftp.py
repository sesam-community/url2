import ftplib
import os
import logging
import io

logger = logging.getLogger('ftp')


class Ftp:
    def __init__(self):
        pass

    def open_session(self):
        return FtpSession()


class FtpSession:
    def __init__(self):
        self._connection = ftp_connect()
        logger.info("Opened connection")

    def read(self, path, args):
        return ftp_get_file(self._connection, path, args=args)

    def write(self, path, stream, args):
        ftp_savefile(self._connection, path, stream=stream)

    def close(self):
        self._connection.quit()
        logger.info("Closed connection")


def ftp_connect():
    try:
        ftp = ftplib.FTP()
        ftp.connect(host=os.environ.get('hostname'), port=int(os.environ.get('ftp_port')))
        logger.info("Logging into %s", os.environ.get('ftp_server'))
        ftp.login(os.environ.get('username'), os.environ.get('password'))
        return ftp
    except ftplib.all_errors as e:
        logger.info('Unable to connect!,%s' % e)


def ftp_savefile(connection,path,stream):
    connection.storbinary('STOR ' + path, io.BytesIO(stream))  # send the file


def ftp_get_file(ftp, path, args):
    is_folder = False
    login_directory =ftp.pwd()
    bio = io.BytesIO()

    def handle_binary(more_data):
        bio.write(more_data)
    try:
        ftp.cwd(path)
        is_folder=True
        logger.info("Path provided is folder - switching to path %s", path)
    except ftplib.error_perm:
        logger.info("connecting to folder %s", path)

    try:
        if is_folder:
            files = ftp.nlst()
        else:
            files = ftp.nlst(path)
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            raise FileNotFoundError("No files in this directory")
        raise resp
    if len(files) > 1:
        raise FileNotFoundError("Path %s resolves to more than one file", path)

    logger.info("Fetching binary from path %s", files[0])
    ftp.retrbinary("RETR " + files[0], callback=handle_binary)
    if args.get('delete_file') == "true":
        logger.info("delete_file property is set to true - deleting file %s", files[0] )
        ftp.delete(files[0])
    # TODO do we need this?
    ftp.cwd(login_directory)
    bio.seek(0)
    return bio
