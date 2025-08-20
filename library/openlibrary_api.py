import httpx

def get_book_info_by_isbn(isbn):
    """
    Open Library API'den ISBN ile kitap bilgilerini çeker.
    
    Args:
        isbn (str): Aranacak kitabın ISBN numarası.
    
    Returns:
        tuple: (success, data_or_message)
               - success (bool): İşlemin başarılı olup olmadığı.
               - data_or_message (dict|str): Başarılıysa kitap bilgileri sözlüğü,
                                             başarısızsa hata mesajı.
    """
    api_url = f"https://openlibrary.org/isbn/{isbn}.json"
    
    try:
        response = httpx.get(api_url, timeout=10, follow_redirects=True)
        
        if response.status_code >= 200 and response.status_code < 300:
            data = response.json()
            
            author_name = 'Yazar bulunamadı'
            
            authors_data = data.get('authors', [])
            if authors_data and isinstance(authors_data, list):
                author_key = authors_data[0].get('key') if authors_data[0] else None
                if author_key:
                    try:
                        author_response = httpx.get(
                            f"https://openlibrary.org{author_key}.json", 
                            timeout=5, 
                            follow_redirects=True
                        )
                        if author_response.status_code >= 200 and author_response.status_code < 300:
                            author_data = author_response.json()
                            author_name = author_data.get('name', author_data.get('personal_name', 'Yazar bulunamadı'))
                    except Exception:
                        pass
            
            if author_name == 'Yazar bulunamadı':
                try:
                    books_api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
                    books_response = httpx.get(books_api_url, timeout=5, follow_redirects=True)
                    if books_response.status_code >= 200 and books_response.status_code < 300:
                        books_data = books_response.json()
                        isbn_key = f"ISBN:{isbn}"
                        if isbn_key in books_data and 'authors' in books_data[isbn_key]:
                            authors_list = books_data[isbn_key]['authors']
                            if authors_list and len(authors_list) > 0:
                                author_name = authors_list[0].get('name', 'Yazar bulunamadı')
                except Exception:
                    pass

            book_info = {
                'title': data.get('title', 'Başlık bulunamadı'),
                'author': author_name,
                'isbn': isbn
            }
            
            return True, book_info
        
        elif response.status_code == 404:
            return False, f"ISBN '{isbn}' için kitap bulunamadı."
        else:
            return False, f"API isteği başarısız oldu: {response.status_code}"

    except httpx.TimeoutException:
        return False, "API isteği zaman aşımına uğradı."
    except httpx.RequestError:
        return False, "API'ye bağlanılamadı. Lütfen internet bağlantınızı kontrol edin."
    except Exception as e:
        return False, f"Beklenmedik bir hata oluştu: {e}"