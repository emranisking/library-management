def test_borrow_available_book(client, make_book):
    book = make_book()
    res = client.post(f"/api/books/{book['id']}/borrow", json={"borrower_name": "  Alice  "})
    assert res.status_code == 200
    body = res.get_json()
    assert body["is_borrowed"] is True
    assert body["borrower_name"] == "Alice"


def test_borrow_same_book_twice_returns_409(client, make_book):
    book = make_book()
    url = f"/api/books/{book['id']}/borrow"
    assert client.post(url, json={"borrower_name": "Alice"}).status_code == 200
    res = client.post(url, json={"borrower_name": "Bob"})
    assert res.status_code == 409
    assert res.get_json() == {"error": "Book is already borrowed"}
    # first borrower is unchanged
    assert client.get(f"/api/books/{book['id']}").get_json()["borrower_name"] == "Alice"


def test_borrow_without_name_returns_400(client, make_book):
    book = make_book()
    res = client.post(f"/api/books/{book['id']}/borrow", json={"borrower_name": "   "})
    assert res.status_code == 400
    assert res.get_json() == {"error": "Borrower name is required"}


def test_borrow_nonexistent_book_returns_404(client):
    res = client.post("/api/books/42/borrow", json={"borrower_name": "Alice"})
    assert res.status_code == 404
