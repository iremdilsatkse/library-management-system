import json

class Book:
    def __init__(self, title, author, isbn):
        """
        Book sınıfının başlatıcısı.
        
        Args:
            title (str): Kitabın başlığı.
            author (str): Kitabın yazarı.
            isbn (str): Kitabın benzersiz ISBN numarası.
        """
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        """Kitabın bilgilerini okunaklı bir string olarak döndürür."""
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def to_dict(self):
        """Book nesnesini JSON formatına uygun bir sözlüğe dönüştürür."""
        return self.__dict__

    @classmethod
    def from_dict(cls, book_dict):
        """Bir sözlükten Book nesnesi oluşturur."""
        return cls(**book_dict)