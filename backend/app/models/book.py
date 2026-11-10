from datetime import datetime, timezone

from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    published_year = db.Column(db.Integer, nullable=False)
    is_borrowed = db.Column(db.Boolean, nullable=False, default=False)
    borrower_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)

    __table_args__ = (
        # Consistency rule: a book is borrowed  <=>  it has a borrower.
        db.CheckConstraint(
            "(is_borrowed = 0 AND borrower_name IS NULL) OR "
            "(is_borrowed = 1 AND borrower_name IS NOT NULL)",
            name="ck_books_borrow_consistency",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "published_year": self.published_year,
            "is_borrowed": self.is_borrowed,
            "borrower_name": self.borrower_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Book {self.id} {self.title!r}>"
