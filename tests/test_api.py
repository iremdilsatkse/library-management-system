import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api import app, library

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_library():
    """Her testten önce kütüphaneyi temizler."""
    library.books = []
    yield
    library.books = []

def test_get_books_empty():
    """Boş kütüphanede kitap listesini test eder."""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_get_books_with_data():
    """Dolu kütüphanede kitap listesini test eder."""
    from library.book import Book
    test_book = Book("Test Kitap", "Test Yazar", "123456789")
    library.add_book(test_book)
    
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Kitap"
    assert data[0]["author"] == "Test Yazar"
    assert data[0]["isbn"] == "123456789"

@patch('library.openlibrary_api.get_book_info_by_isbn')
def test_add_book_success(mock_api):
    """Başarılı kitap eklemeyi test eder."""
    mock_api.return_value = (True, {
        'title': '1984',
        'author': 'George Orwell',
        'isbn': '978-0451524935'
    })
    
    response = client.post("/books", json={"isbn": "978-0451524935"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert data["isbn"] == "978-0451524935"

@patch('library.openlibrary_api.get_book_info_by_isbn')
def test_add_book_not_found(mock_api):
    """Bulunamayan kitap eklemeyi test eder."""
    mock_api.return_value = (False, "ISBN '123' için kitap bulunamadı.")
    
    response = client.post("/books", json={"isbn": "123"})
    assert response.status_code == 404
    assert "bulunamadı" in response.json()["detail"]

@patch('library.openlibrary_api.get_book_info_by_isbn')
def test_add_existing_book(mock_api):
    """Zaten var olan kitap eklemeyi test eder."""
    from library.book import Book
    existing_book = Book("Mevcut Kitap", "Mevcut Yazar", "978-0451524935")
    library.add_book(existing_book)
    
    mock_api.return_value = (True, {
        'title': '1984',
        'author': 'George Orwell',
        'isbn': '978-0451524935'
    })
    
    response = client.post("/books", json={"isbn": "978-0451524935"})
    assert response.status_code == 400
    assert "zaten mevcut" in response.json()["detail"]

def test_delete_book_success():
    """Başarılı kitap silmeyi test eder."""
    from library.book import Book
    test_book = Book("Silinecek Kitap", "Test Yazar", "978-0451524935")
    library.add_book(test_book)
    
    response = client.delete("/books/978-0451524935")
    assert response.status_code == 200
    assert "silindi" in response.json()["message"]

def test_delete_book_not_found():
    """Bulunamayan kitap silmeyi test eder."""
    response = client.delete("/books/non-existent-isbn")
    assert response.status_code == 404
    assert "bulunamadı" in response.json()["detail"]