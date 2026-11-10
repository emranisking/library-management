def test_return_borrowed_book(client, make_book):
    book = make_book()
    client.post(f"/api/books/{book['id']}/borrow", json={"borrower_name": "Alice"})
    res = client.post(f"/api/books/{book['id']}/return")
    assert res.status_code == 200
    body = res.get_json()
    assert body["is_borrowed"] is False
    assert body["borrower_name"] is None


def test_return_available_book_returns_409(client, make_book):
    book = make_book()
    res = client.post(f"/api/books/{book['id']}/return")
    assert res.status_code == 409
    assert "error" in res.get_json()


def test_return_nonexistent_book_returns_404(client):
    assert client.post("/api/books/42/return").status_code == 404
