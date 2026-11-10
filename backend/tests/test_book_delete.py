def test_delete_available_book(client, make_book):
    book = make_book()
    res = client.delete(f"/api/books/{book['id']}")
    assert res.status_code == 204
    assert res.data == b""
    assert client.get(f"/api/books/{book['id']}").status_code == 404


def test_delete_borrowed_book_returns_409(client, make_book):
    book = make_book()
    client.post(f"/api/books/{book['id']}/borrow", json={"borrower_name": "Alice"})
    res = client.delete(f"/api/books/{book['id']}")
    assert res.status_code == 409
    assert "error" in res.get_json()
    assert client.get(f"/api/books/{book['id']}").status_code == 200


def test_delete_nonexistent_book_returns_404(client):
    assert client.delete("/api/books/999").status_code == 404
