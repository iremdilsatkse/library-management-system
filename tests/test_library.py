import json
import os
import pytest
from library.book import Book
from library.library import Library

@pytest.fixture
def empty_library():
    """Boş bir kütüphane nesnesi oluşturur ve test bitiminde dosyayı temizler."""
    data_file = 'test_library.json'
    if os.path.exists(data_file):
        os.remove(data_file)
    library = Library(data_file)
    yield library
    if os.path.exists(data_file):
        os.remove(data_file)

@pytest.fixture
def populated_library(empty_library):
    """İçinde bir kitap olan kütüphane nesnesi oluşturur."""
    book = Book('1984', 'George Orwell', '978-0451524935')
    empty_library.add_book(book)
    return empty_library

def test_add_book(empty_library):
    """Kitap ekleme işlevini test eder."""
    book = Book('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', '978-0345391803')
    success, message = empty_library.add_book(book)
    assert success is True
    assert 'eklendi' in message
    assert len(empty_library.books) == 1
    assert empty_library.books[0].title == 'The Hitchhiker\'s Guide to the Galaxy'


def test_add_existing_book_fails(populated_library):
    """Zaten var olan bir ISBN ile kitap eklenemediğini test eder."""
    book = Book('New Title', 'New Author', '978-0451524935')
    success, message = populated_library.add_book(book)
    assert success is False
    assert 'zaten mevcut' in message
    assert len(populated_library.books) == 1


def test_remove_book(populated_library):
    """Kitap silme işlevini test eder."""
    success, message = populated_library.remove_book('978-0451524935')
    assert success is True
    assert 'silindi' in message
    assert len(populated_library.books) == 0


def test_remove_non_existing_book(populated_library):
    """Var olmayan bir kitabı silmeye çalışmayı test eder."""
    success, message = populated_library.remove_book('non-existent-isbn')
    assert success is False
    assert 'bulunamadı' in message
    assert len(populated_library.books) == 1


def test_find_book(populated_library):
    """Kitap arama işlevini test eder."""
    found_book = populated_library.find_book('978-0451524935')
    assert found_book is not None
    assert found_book.title == '1984'
    assert found_book.author == 'George Orwell'


def test_find_non_existing_book(populated_library):
    """Var olmayan bir kitabı aramayı test eder."""
    found_book = populated_library.find_book('non-existent-isbn')
    assert found_book is None


def test_list_books_empty(empty_library):
    """Boş kütüphaneyi listeleme işlevini test eder."""
    output = empty_library.list_books()
    assert 'henüz kitap yok' in output


def test_list_books_populated(populated_library):
    """Dolu kütüphaneyi listeleme işlevini test eder."""
    output = populated_library.list_books()
    assert '1984 by George Orwell' in output
    assert 'Kütüphanedeki Kitaplar' in output


def test_data_persistence(populated_library):
    """Uygulama yeniden başlatıldığında verilerin kalıcı olduğunu test eder."""
    populated_library.save_books()
    
    new_library = Library(populated_library.data_file)
    assert len(new_library.books) == 1
    assert new_library.books[0].title == '1984'