import os

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import logging

logger = logging.getLogger('ssh')


class Ssh:
    def __init__(self):
        pass

    def open_session(self):
        return SshSession()


class SshSession:
    def __init__(self):
        self._connection = ssh_connect()
        logger.info("Opened connection")

    def read(self, path, args):
        return ssh_get_file(self._connection, path, args=args)

    def write(self, path, stream, args):
        ssh_savefile(self._connection, path, stream=stream)

    def close(self):
        self._connection.close()
        logger.info("Closed connection")


def ssh_connect():
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hostname=os.environ.get('hostname'),
                   username=os.environ.get('username'),
                   password=os.environ.get('password'))
    return client


def ssh_savefile(connection, path, stream):
    pass


def ssh_get_file(connection, path, args):
    stdin, stdout, stderr = connection.exec_command('cat ' + path)
    return stdout
