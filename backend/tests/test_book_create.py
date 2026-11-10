from datetime import datetime

VALID = {
    "title": "Clean Code",
    "author": "Robert Martin",
    "category": "Technology",
    "published_year": 2008,
}


def test_create_valid_book(client):
    res = client.post("/api/books", json=VALID)
    assert res.status_code == 201
    body = res.get_json()
    assert body["id"] == 1
    assert body["title"] == "Clean Code"
    assert body["is_borrowed"] is False
    assert body["borrower_name"] is None
    assert body["created_at"]


def test_create_without_title(client):
    res = client.post("/api/books", json={**VALID, "title": ""})
    assert res.status_code == 400
    assert res.get_json() == {"error": "Title is required"}
    assert client.get("/api/books").get_json() == []


def test_create_without_author(client):
    payload = {k: v for k, v in VALID.items() if k != "author"}
    res = client.post("/api/books", json=payload)
    assert res.status_code == 400
    assert res.get_json() == {"error": "Author is required"}


def test_year_below_1900(client):
    res = client.post("/api/books", json={**VALID, "published_year": 1899})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_year_in_future(client):
    future = datetime.now().year + 1
    res = client.post("/api/books", json={**VALID, "published_year": future})
    assert res.status_code == 400


def test_year_wrong_type(client):
    res = client.post("/api/books", json={**VALID, "published_year": "2008"})
    assert res.status_code == 400


def test_non_object_body(client):
    res = client.post("/api/books", json=["not", "an", "object"])
    assert res.status_code == 400
    assert res.get_json() == {"error": "Request body must be a JSON object"}


def test_invalid_json_body(client):
    res = client.post("/api/books", data="{bad", content_type="application/json")
    assert res.status_code == 400
    assert res.is_json


def test_get_existing_book(client, make_book):
    book = make_book()
    res = client.get(f"/api/books/{book['id']}")
    assert res.status_code == 200
    assert res.get_json()["title"] == "Clean Code"


def test_get_nonexistent_book(client):
    res = client.get("/api/books/999")
    assert res.status_code == 404
    assert res.get_json() == {"error": "Book not found"}


def test_unknown_route_returns_json_404(client):
    res = client.get("/api/nope")
    assert res.status_code == 404
    assert res.is_json


def test_method_not_allowed_returns_json_405(client):
    res = client.patch("/api/books")
    assert res.status_code == 405
    assert res.is_json


def test_search_and_filter(client, make_book):
    make_book(title="Clean Code", author="Robert Martin", category="Technology")
    make_book(title="The Hobbit", author="Tolkien", category="Fiction", published_year=1937)

    assert len(client.get("/api/books?search=clean").get_json()) == 1
    assert len(client.get("/api/books?search=TOLKIEN").get_json()) == 1
    assert len(client.get("/api/books?category=Fiction").get_json()) == 1
    assert len(client.get("/api/books?search=clean&category=Fiction").get_json()) == 0
    assert len(client.get("/api/books").get_json()) == 2


def test_categories_endpoint(client, make_book):
    make_book(category="Technology")
    make_book(category="Fiction")
    assert client.get("/api/books/categories").get_json() == ["Fiction", "Technology"]
