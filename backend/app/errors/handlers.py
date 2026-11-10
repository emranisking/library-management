import logging

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from app.errors.exceptions import AppError
from app.extensions import db

logger = logging.getLogger(__name__)


def _json_error(message, status):
    return jsonify({"error": message}), status


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err):
        return _json_error(err.message, err.status_code)

    @app.errorhandler(HTTPException)
    def handle_http_error(err):
        # Covers Flask's default 404 / 405 / 415 ... so we never return HTML.
        return _json_error(err.description or err.name, err.code or 500)

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(err):
        db.session.rollback()
        logger.exception("Database error: %s", err)
        return _json_error("Database error", 500)

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        db.session.rollback()
        logger.exception("Unexpected error: %s", err)
        return _json_error("Internal server error", 500)
