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
    client.connect(hostname=os.environ.get('hostname'),
                   username=os.environ.get('username'),
                   password=os.environ.get('password'))
    return client


def savefile(connection, path, stream):
    connection.exec_command('echo ' + str(stream) + ' >> ' + path + '\n')


def get_files(connection, path, args):
    streams = []
    filenames = []

    filetype = path.split(".")[-1]
    stdin, stdout, stderr = connection.exec_command('ls ' + path)
    for out in stdout.readlines():
        filenames.append(out)
    for name in filenames:
        name = name.replace('\n', '')
        if name.split(".")[-1] == args.get('type', filetype).lower():
            if len(filenames)>1:
                logger.info("Found file: %s" % name)
                stdin, stdout, stderr = connection.exec_command('cat ' + path + str(name))
            else :
                logger.info("Found file: %s" % path)
                stdin, stdout, stderr = connection.exec_command('cat ' + path)
            streams.append(stdout)
    return streams
