from datetime import datetime

from app.errors.exceptions import ValidationError

MIN_YEAR = 1900


def _require_object(payload):
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object")
    return payload


def _required_string(payload, field, label):
    value = payload.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{label} is required")
    if not isinstance(value, str):
        raise ValidationError(f"{label} must be a string")
    return value.strip()


def validate_book_payload(payload):
    """Validate a create / update body and return a cleaned dict."""
    payload = _require_object(payload)

    title = _required_string(payload, "title", "Title")
    author = _required_string(payload, "author", "Author")

    category = payload.get("category")
    if category is not None:
        if not isinstance(category, str):
            raise ValidationError("Category must be a string")
        category = category.strip() or None

    year = payload.get("published_year")
    if year is None or year == "":
        raise ValidationError("Published year is required")
    # bool is a subclass of int - reject it explicitly.
    if isinstance(year, bool) or not isinstance(year, int):
        raise ValidationError("Published year must be an integer")
    current_year = datetime.now().year
    if year < MIN_YEAR or year > current_year:
        raise ValidationError(
            f"Published year must be between {MIN_YEAR} and {current_year}"
        )

    return {
        "title": title,
        "author": author,
        "category": category,
        "published_year": year,
    }


def validate_borrow_payload(payload):
    payload = _require_object(payload)
    return _required_string(payload, "borrower_name", "Borrower name")
