import json
import os
from .book import Book
from .openlibrary_api import get_book_info_by_isbn 

class Library:
    def __init__(self, data_file='library.json'):
        self.data_file = data_file
        self.books = self.load_books()

    def add_book(self, book):
        """Book nesnesi ile kitap ekler."""
        if any(b.isbn == book.isbn for b in self.books):
            return False, "Bu ISBN'ye sahip bir kitap zaten mevcut."
        self.books.append(book)
        self.save_books()
        return True, f"'{book.title}' kütüphaneye eklendi."

    def remove_book(self, isbn):
        """ISBN ile kitap siler."""
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.isbn != isbn]
        if len(self.books) < initial_count:
            self.save_books()
            return True, "Kitap başarıyla silindi."
        return False, "Kitap bulunamadı veya silinemedi."

    def get_books(self):
        """Tüm kitapları döndürür (API için)"""
        return self.books

    def list_books(self):
        """Kitapları string formatında listeler."""
        if not self.books:
            return "Kütüphanede henüz kitap yok."
        
        book_list_str = "Kütüphanedeki Kitaplar:\n"
        for book in self.books:
            book_list_str += f"- {book}\n"
        return book_list_str.strip()

    def find_book(self, isbn):
        """ISBN ile kitap bulur."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def load_books(self):
        """JSON dosyasından kitapları yükler."""
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Book.from_dict(d) for d in data]
        except (IOError, json.JSONDecodeError):
            return []

    def save_books(self):
        """Kitapları JSON dosyasına kaydeder."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4, ensure_ascii=False)

    def add_book_by_isbn(self, isbn):
        """ISBN ile kitap ekler."""
        success, data_or_message = get_book_info_by_isbn(isbn)
        if success:
            new_book = Book(data_or_message['title'], data_or_message['author'], data_or_message['isbn'])
            return self.add_book(new_book)
        else:
            return False, data_or_message