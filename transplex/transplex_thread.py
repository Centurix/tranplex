import threading
import logging
from flask import (
    Flask,
    current_app
)
from werkzeug.serving import make_server
from resources import test_resource
from plexapi.myplex import MyPlexAccount


class TransplexThread(threading.Thread):
    def __init__(self, host, port, plex_user, plex_password, plex_server):
        threading.Thread.__init__(self)
        self._app = Flask(__name__)

        with self._app.app_context():
            current_app.plex_account = MyPlexAccount(plex_user, plex_password)
            current_app.plex_resource = current_app.plex_account.resource(
                plex_server
            ).connect()
            logging.info(
                f"Connecting to PLEX server {plex_server} with user {plex_user}"
            )

        self._app.register_blueprint(test_resource)
        self.srv = make_server(host, port, self._app)
        self.ctx = self._app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
