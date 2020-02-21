#!/usr/bin/env python3
import click
import signal
import platform
import logging
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
    """
    # Both Linux and Windows signals
    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)

    if platform.system() == "Linux":  # Linux only
        signal.signal(signal.SIGQUIT, stop_server)
        signal.signal(signal.SIGHUP, stop_server)


@click.command()
@click.option("-i", "--interactive", default=False, is_flag=True, help="Interactive")
@click.option(
    "-b",
    "--bind",
    envvar="TRANSPLEX_BIND",
    default="127.0.0.1",
    help="Bound interface"
)
@click.option(
    "-p",
    "--port",
    envvar="TRANSPLEX_PORT",
    default=5123,
    help="Bound port"
)
def main(interactive, bind, port):
    """
    Add a rotating log handler and start the main thread plus interactive
    console if needed
    :return:
    """
    global server_semaphore
    set_log_handler("transplex.log")

    logging.info(f"Starting TransPLEX with {interactive}, {bind}, {port}")

    server = TransplexThread(bind, port)
    server.start()

    click.echo(
        f"Starting {click.style('Trans', fg='red', bold=True)}"
        f"PLE{click.style('X', fg='yellow', bold=True)} "
        f"on {platform.system()} "
        f"at http://{bind}:{port}"
    )

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
