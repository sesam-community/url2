import logging

logger  = logging.getLogger('sshfs')


class Ftp:
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
        self._connection.quit()
        logger.info("Closed connection")


def ssh_connect():
    pass


def ssh_savefile(connection, path, stream):
    pass


def ssh_get_file(connection, path, args):
    pass


def ssh_savefile(connection, path, stream):
    pass