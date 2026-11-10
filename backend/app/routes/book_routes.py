from flask import Blueprint, request

from app.services.book_service import BookService
from app.utils.responses import created, no_content, ok
from app.validators.book_validator import (
    validate_book_payload,
    validate_borrow_payload,
)

book_bp = Blueprint("books", __name__)


def _json_body():
    return request.get_json(silent=True)


@book_bp.get("")
def list_books():
    books = BookService.get_all_books(
        search=request.args.get("search"),
        category=request.args.get("category"),
    )
    return ok([b.to_dict() for b in books])


@book_bp.get("/categories")
def list_categories():
    return ok(BookService.get_categories())


@book_bp.post("")
def create_book():
    data = validate_book_payload(_json_body())
    return created(BookService.create_book(data).to_dict())


@book_bp.get("/<int:book_id>")
def get_book(book_id):
    return ok(BookService.get_book_by_id(book_id).to_dict())


@book_bp.put("/<int:book_id>")
def update_book(book_id):
    data = validate_book_payload(_json_body())
    return ok(BookService.update_book(book_id, data).to_dict())


@book_bp.delete("/<int:book_id>")
def delete_book(book_id):
    BookService.delete_book(book_id)
    return no_content()


@book_bp.post("/<int:book_id>/borrow")
def borrow_book(book_id):
    name = validate_borrow_payload(_json_body())
    return ok(BookService.borrow_book(book_id, name).to_dict())


@book_bp.post("/<int:book_id>/return")
def return_book(book_id):
    return ok(BookService.return_book(book_id).to_dict())
