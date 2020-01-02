import threading
import flask
from werkzeug.serving import make_server
from resources import test_resource


class TransplexThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self._app = flask.Flask(__name__)
        self._app.register_blueprint(test_resource)
        self.srv = make_server(host, port, self._app)
        self.ctx = self._app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
