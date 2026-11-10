def test_update_book(client, make_book):
    book = make_book()
    res = client.put(
        f"/api/books/{book['id']}",
        json={
            "title": "Clean Architecture",
            "author": "Robert Martin",
            "category": "Technology",
            "published_year": 2017,
        },
    )
    assert res.status_code == 200
    assert res.get_json()["title"] == "Clean Architecture"
    assert res.get_json()["published_year"] == 2017


def test_update_keeps_borrow_state(client, make_book):
    book = make_book()
    client.post(f"/api/books/{book['id']}/borrow", json={"borrower_name": "Alice"})
    res = client.put(
        f"/api/books/{book['id']}",
        json={"title": "New", "author": "Auth", "category": None, "published_year": 2000},
    )
    assert res.status_code == 200
    assert res.get_json()["is_borrowed"] is True
    assert res.get_json()["borrower_name"] == "Alice"


def test_update_invalid_returns_400(client, make_book):
    book = make_book()
    res = client.put(
        f"/api/books/{book['id']}",
        json={"title": "", "author": "A", "published_year": 2000},
    )
    assert res.status_code == 400


def test_update_nonexistent_book_returns_404(client):
    res = client.put(
        "/api/books/999",
        json={"title": "T", "author": "A", "category": "C", "published_year": 2000},
    )
    assert res.status_code == 404
