import cmd2
import click
import logging


class ConsoleApp(cmd2.Cmd):
    def __init__(self, flask_thread):
        super().__init__(allow_cli_args=False)
        self._flask_thread = flask_thread

    def do_quit(self, _):
        """Exit this application"""
        self._flask_thread.shutdown()
        return True

    def do_logs(self, args):
        """
        Grab the logs from the rotating log handler
        :param args:
        :return:
        """
        log = logging.getLogger("werkzeug")
        if len(log.handlers) > 0:
            with open(log.handlers[0].baseFilename, "r") as log_file:
                click.echo(log_file.read())
