from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from app.errors.exceptions import ConflictError, NotFoundError
from app.extensions import db
from app.models.book import Book


def _commit():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


class BookService:
    """All book business rules and database operations."""

    @staticmethod
    def get_all_books(search=None, category=None):
        query = Book.query
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(Book.title.ilike(term), Book.author.ilike(term))
            )
        if category and category.strip():
            query = query.filter(Book.category.ilike(category.strip()))
        return query.order_by(Book.id.asc()).all()

    @staticmethod
    def get_categories():
        rows = (
            db.session.query(Book.category)
            .filter(Book.category.isnot(None))
            .distinct()
            .order_by(Book.category.asc())
            .all()
        )
        return [r[0] for r in rows]

    @staticmethod
    def get_book_by_id(book_id):
        book = db.session.get(Book, book_id)
        if book is None:
            raise NotFoundError("Book not found")
        return book

    @staticmethod
    def create_book(data):
        book = Book(**data, is_borrowed=False, borrower_name=None)
        db.session.add(book)
        _commit()
        return book

    @staticmethod
    def update_book(book_id, data):
        book = BookService.get_book_by_id(book_id)
        book.title = data["title"]
        book.author = data["author"]
        book.category = data["category"]
        book.published_year = data["published_year"]
        _commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = BookService.get_book_by_id(book_id)
        if book.is_borrowed:
            raise ConflictError("Cannot delete a book that is currently borrowed")
        db.session.delete(book)
        _commit()

    @staticmethod
    def borrow_book(book_id, borrower_name):
        book = BookService.get_book_by_id(book_id)
        if book.is_borrowed:
            raise ConflictError("Book is already borrowed")
        book.is_borrowed = True
        book.borrower_name = borrower_name.strip()
        _commit()
        return book

    @staticmethod
    def return_book(book_id):
        book = BookService.get_book_by_id(book_id)
        if not book.is_borrowed:
            raise ConflictError("Book is not currently borrowed")
        book.is_borrowed = False
        book.borrower_name = None
        _commit()
        return book
