import pytest
import httpx
from unittest.mock import patch, Mock
from library.openlibrary_api import get_book_info_by_isbn

def mock_httpx_get_success(*args, **kwargs):
    """Başarılı bir API isteğini taklit eder."""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        
        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if 'isbn' in args[0]:
        return MockResponse({
            'title': 'The Lord of the Rings',
            'authors': [{'key': '/authors/OL23919A'}],
            'isbn': '9780547928227'
        }, 200)
    elif 'authors' in args[0]:
        return MockResponse({
            'name': 'J.R.R. Tolkien'
        }, 200)
    
    return MockResponse({}, 404)

def mock_httpx_get_404(*args, **kwargs):
    """404 hatasını taklit eder."""
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code
        
        def json(self):
            return {}
        
        def raise_for_status(self):
            raise httpx.HTTPStatusError('Not Found', request=None, response=self)

    return MockResponse(404)

def mock_httpx_get_request_error(*args, **kwargs):
    """İnternet bağlantı hatasını taklit eder."""
    raise httpx.RequestError('Connection Error', request=None)

@patch('openlibrary_api.httpx.get', side_effect=mock_httpx_get_success)
def test_get_book_info_success(mock_get):
    """API'den başarılı bir şekilde kitap bilgisi çekmeyi test eder."""
    success, result = get_book_info_by_isbn('9780547928227')
    
    assert success is True
    assert isinstance(result, dict)
    assert result['title'] == 'The Lord of the Rings'
    assert result['author'] == 'J.R.R. Tolkien'
    assert result['isbn'] == '9780547928227'
    assert mock_get.call_count == 2 

@patch('openlibrary_api.httpx.get', side_effect=mock_httpx_get_404)
def test_get_book_info_not_found(mock_get):
    """Geçersiz bir ISBN girildiğinde hatayı test eder."""
    success, message = get_book_info_by_isbn('non-existent-isbn')
    
    assert success is False
    assert 'bulunamadı' in message

@patch('openlibrary_api.httpx.get', side_effect=mock_httpx_get_request_error)
def test_get_book_info_connection_error(mock_get):
    """API bağlantı hatasını test eder."""
    success, message = get_book_info_by_isbn('9780547928227')
    
    assert success is False
    assert 'bağlanılamadı' in message