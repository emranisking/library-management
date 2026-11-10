from flask import Flask

from app.errors.handlers import register_error_handlers
from app.extensions import cors, db
from app.routes.book_routes import book_bp


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or "app.config.settings.Config")

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    register_error_handlers(app)
    app.register_blueprint(book_bp, url_prefix="/api/books")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
