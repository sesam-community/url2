import os
import logger
from paramiko import SSHClient, AutoAddPolicy

logger = logger.Logger("ssh")


class Ssh:
    def __init__(self):
        pass

    def open_session(self):
        return SshSession()


class SshSession:
    def __init__(self):
        self._connection = connect()
        logger.info("Opened connection")

    def read(self, path, args):
        return get_files(self._connection, path, args=args)

    def write(self, path, stream, args):
        savefile(self._connection, path, stream=stream)

    def close(self):
        self._connection.close()
        logger.info("Closed connection")


def connect():
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    logger.info("Logging into %s" % os.environ.get('hostname'))
    try:
        client.connect(hostname=os.environ.get('hostname'), username=os.environ.get('username'), password=os.environ.get('password'))
    except Exception as e:
        logger.info("could not connect to " +os.environ.get('hostname')+ ":  %s" % e)
        raise Exception("Problem connecting : '%s'" % e)
    return client


def savefile(connection, path, stream):
    dir = path.split('/')
    p = ""
    for element in dir:
        if not element == dir[-1]:
            p = p + element + "/"
    connection.exec_command('if [ -f '  + path + ' ]; then echo \"' + stream.decode() + '\" >> ' + path + ' ; else mkdir -p ' + p + ' ; echo \"'+ stream.decode() + '\" >> ' + path + ' ; fi')


def get_files(connection, path, args):
    streams = []
    filenames = []

    filetype = path.split(".")[-1]
    stdin, stdout, stderr = connection.exec_command('ls ' + path)
    is_folder = connection.exec_command('if [ -d ' + path + ' ] ; then echo true; else echo false; fi')[1].readlines()[0].replace('\n', '')
    stdin, stdout, stderr = connection.exec_command('ls ' + path)
    if is_folder == "true":
        for out in stdout.readlines():
            filenames.append(out)
        for name in filenames:
            name = name.replace('\n', '')
            if name.split(".")[-1] == args.get('type', filetype).lower():
                logger.info("Found file: %s" % name)
                stdin, stdout, stderr = connection.exec_command('cat ' + path + str(name))
                streams.append(stdout)
    else :
            logger.info("Found file: %s" % path)
            stdin, stdout, stderr = connection.exec_command('cat ' + path)
            streams.append(stdout)

    return streams
