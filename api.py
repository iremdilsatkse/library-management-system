# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library.book import Book
from library.library import Library
from library.openlibrary_api import get_book_info_by_isbn

app = FastAPI(title="Library API", description="Kitap Kütüphanesi API'si", version="1.0.0")
library = Library()

class ISBNRequest(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

# GET /books → Kütüphanedeki tüm kitaplar
@app.get("/books", response_model=list[BookResponse])
def get_books():
    books = library.books  
    return [BookResponse(title=book.title, author=book.author, isbn=book.isbn) for book in books]

# POST /books → ISBN ile kitap ekle
@app.post("/books", response_model=BookResponse)
def add_book(isbn_request: ISBNRequest):
    isbn = isbn_request.isbn
    success, data_or_message = get_book_info_by_isbn(isbn)

    if not success:
        raise HTTPException(status_code=404, detail=data_or_message)

    book = Book(data_or_message['title'], data_or_message['author'], data_or_message['isbn'])
    
    success, message = library.add_book(book)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return BookResponse(title=book.title, author=book.author, isbn=book.isbn)

# DELETE /books/{isbn} → Kitabı sil
@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    success, message = library.remove_book(isbn)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}