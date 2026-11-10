from flask import jsonify


def ok(data, status=200):
    """JSON success response."""
    return jsonify(data), status


def created(data):
    return ok(data, 201)


def no_content():
    """204 with an empty body, as required by the DELETE contract."""
    return "", 204
