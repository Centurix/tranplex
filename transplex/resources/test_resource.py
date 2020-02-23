from flask import Blueprint
from flask import make_response
from flask import abort
from flask import current_app


test_resource = Blueprint('test_resource', __name__)


"""
How to capture and send JSONAPI errors from exceptions
How to set JSONAPI headers correctly
How to properly send information from transformers
"""


@test_resource.route("/", methods=("OPTION",))
def preflight():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def jsonapi_headers():
    response = make_response()
    response.headers.add("Content-Type", "application/vnd.api+json")
    return response


@test_resource.errorhandler(404)
def not_found_exception(e):
    return "NOT FOUND"


@test_resource.route("/", methods=("GET",))
def list_all():
    """
    Lets list all libraries in Plex
    :return:
    """
    items = list()
    plex = current_app.plex_resource

    for section in plex.library.sections():
        items.append(section.title)

    return '\n'.join(items)


@test_resource.route("/<resource_id>", methods=("GET",))
def return_one(resource_id):
    abort(405, "Resource not found")
    return f"THIS IS ONE RESOURCE FOR {resource_id}"
