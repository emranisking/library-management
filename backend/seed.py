"""Insert 10 sample books (only when the table is empty unless --force)."""
import sys

from app import create_app
from app.extensions import db
from app.models.book import Book

SAMPLE_BOOKS = [
    ("Clean Code", "Robert C. Martin", "Technology", 2008, None),
    ("Atomic Habits", "James Clear", "Self-help", 2018, "Alice Johnson"),
    ("The Hobbit", "J.R.R. Tolkien", "Fiction", 1937, None),
    ("Sapiens", "Yuval Noah Harari", "History", 2011, None),
    ("The Pragmatic Programmer", "Andrew Hunt", "Technology", 2019, None),
    ("1984", "George Orwell", "Fiction", 1949, "Bob Smith"),
    ("Deep Work", "Cal Newport", "Self-help", 2016, None),
    ("A Brief History of Time", "Stephen Hawking", "Science", 1988, None),
    ("Dune", "Frank Herbert", "Fiction", 1965, None),
    ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 2011, "Carol White"),
]


def seed(force=False):
    if Book.query.count() > 0 and not force:
        print("Database already contains books - skipping seed.")
        return 0
    for title, author, category, year, borrower in SAMPLE_BOOKS:
        db.session.add(
            Book(
                title=title,
                author=author,
                category=category,
                published_year=year,
                is_borrowed=borrower is not None,
                borrower_name=borrower,
            )
        )
    db.session.commit()
    print(f"Inserted {len(SAMPLE_BOOKS)} sample books.")
    return len(SAMPLE_BOOKS)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        seed(force="--force" in sys.argv)
