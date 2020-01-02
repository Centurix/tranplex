#!/usr/bin/env python3
import click
import signal
from console import ConsoleApp
from transplex.transplex_thread import TransplexThread
from transplex.transplex_log_handler import set_log_handler

"""
Transplex: Transfer files from a Plex library to a USB drive

There are two parts to this project:
1. REST API backend for the file system
2. SPA Frontend to provide a visual process

Uses Flask Blueprints to get things to work
Adds interactive mode to Flask backend

Uses JSONAPI for REST
Uses JSONSCHEMA for validation

"""

EXIT_OK = 0
EXIT_PARAM_ERROR = 1
EXIT_OTHER_ERROR = 2

server_semaphore = True


def stop_server(signal_number, frame):
    global server_semaphore
    server_semaphore = False
    return


def capture_signals():
    """
    Capture Linux signals to exit the non-interactive server
    TODO: Make this respond to Windows signals
    :return:
    """
    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)
    signal.signal(signal.SIGQUIT, stop_server)
    signal.signal(signal.SIGHUP, stop_server)


@click.command()
@click.option("-i", "--interactive", default=False, is_flag=True, help="Interactive")
@click.option("-b", "--bind", default="127.0.0.1", help="Bound interface")
@click.option("-p", "--port", default=5123, help="Bound port")
def main(interactive, bind, port):
    """
    Add a rotating log handler and start the main thread plus interactive
    console if needed
    :return:
    """
    global server_semaphore
    set_log_handler("transplex.log")

    server = TransplexThread(bind, port)
    server.start()

    click.echo(f"Server started at http://{bind}:{port}")

    if interactive:
        console_app = ConsoleApp(server)
        console_app.cmdloop()
    else:
        capture_signals()
        while server_semaphore:
            pass

        server.shutdown()

    click.echo("Server stopped")
    raise click.exceptions.Exit(EXIT_OK)


if __name__ == "__main__":
    main()
