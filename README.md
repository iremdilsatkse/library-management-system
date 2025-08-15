# Kütüphane Yönetim Sistemi

Bu proje, kitap kütüphanelerini yönetmek için geliştirilmiş modern bir uygulamadır. Hem konsol uygulaması hem de REST API desteği sunar.

## 🌟 Özellikler

- **Nesne Yönelimli Tasarım**: Modüler ve sürdürülebilir kod yapısı
- **ISBN ile Otomatik Kitap Ekleme**: Open Library API entegrasyonu
- **RESTful API**: FastAPI ile modern web API desteği
- **Veri Kalıcılığı**: JSON tabanlı veri saklama
- **Kapsamlı Testler**: Pytest ile %100 test kapsamı

## 📋 Sistem Gereksinimleri

- Python 3.8+
- Internet bağlantısı (kitap bilgileri için)

## 🚀 Kurulum

### 1. Projeyi klonlayın
```bash
git clone https://github.com/iremdilsatkse/library-management-system.git
cd library-management-system
```

### 2. Sanal ortam oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Gerekli paketleri yükleyin
```bash
pip install -r requirements.txt
```

## 📁 Proje Yapısı

```
library-management-system/
├── library/
│   ├── __init__.py
│   ├── book.py              # Book sınıfı
│   ├── library.py           # Library sınıfı
│   └── openlibrary_api.py   # Open Library API entegrasyonu
├── tests/
│   ├── test_api.py             # API testleri
│   ├── test_library.py         # Library testleri
│   ├── test_openlibrary_api.py # API entegrasyon testleri
├── api.py                   # FastAPI uygulaması
├── main.py                  # Konsol uygulaması
├── requirements.txt        # Bağımlılıklar
├── library.json           # Veri dosyası (otomatik oluşur)
└── README.md              
```

## 🖥️ Kullanım

### Konsol Uygulaması

Basit konsol arayüzü ile kitap yönetimi:

```bash
python main.py
```

**Menü Seçenekleri:**
1. ISBN ile Kitap Ekle
2. Kitap Sil
3. Kitapları Listele
4. Kitap Ara
5. Çıkış

### REST API

Modern web API ile programatik erişim:

```bash
uvicorn api:app --reload
```

API şu adreste çalışacaktır: `http://127.0.0.1:8000`

**İnteraktif Dokümantasyon:** `http://127.0.0.1:8000/docs`

## 🔌 API Endpoints

### GET /books
Kütüphanedeki tüm kitapları listeler.

**Örnek Response:**
```json
[
  {
    "title": "1984",
    "author": "George Orwell",
    "isbn": "9780451524935"
  }
]
```

### POST /books
ISBN ile yeni kitap ekler.

**Request Body:**
```json
{
  "isbn": "9780451524935"
}
```

**Response:**
```json
{
  "title": "1984",
  "author": "George Orwell",
  "isbn": "9780451524935"
}
```

### DELETE /books/{isbn}
Belirtilen ISBN'e sahip kitabı siler.

**Response:**
```json
{
  "message": "Kitap başarıyla silindi."
}
```

## 🧪 Test

Tüm testleri çalıştırmak için:

```bash
pytest -v
```

Belirli bir test dosyasını çalıştırmak için:

```bash
pytest test_api.py -v
pytest test_library.py -v
pytest test_openlibrary_api.py -v
```

Test kapsamını görmek için:

```bash
pytest --cov=library --cov-report=html
```

## 📖 Test için Geçerli ISBN'ler

- `9780451524935` - 1984 by George Orwell
- `9780547928227` - The Hobbit by J.R.R. Tolkien
- `9780439708180` - Harry Potter and the Sorcerer's Stone
- `9780345391803` - The Hitchhiker's Guide to the Galaxy
- `9780486284736` - Pride and Prejudice by Jane Austen

## 🏗️ Mimari

### Temel Sınıflar

**Book**: Kitap nesnelerini temsil eder
- `title`: Kitap başlığı
- `author`: Yazar adı
- `isbn`: Benzersiz ISBN numarası

**Library**: Kütüphane operasyonlarını yönetir
- Kitap ekleme/silme/arama
- JSON veri kalıcılığı
- Open Library API entegrasyonu

### API Katmanı

**FastAPI**: Modern, hızlı web framework
- Pydantic ile otomatik veri validasyonu
- OpenAPI/Swagger otomatik dokümantasyon
- Tip güvenliği ve IDE desteği

### Veri Katmanı

**JSON Storage**: Basit dosya tabanlı veri saklama
- `library.json` dosyasında kitap verileri
- UTF-8 encoding ile Türkçe karakter desteği
- Otomatik yedekleme ve geri yükleme

## 📞 İletişim

Proje ile ilgili sorularınız için issue oluşturabilirsiniz.

## 🙏 Teşekkürler

- [Open Library](https://openlibrary.org/) - Ücretsiz kitap veritabanı API'si
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Pytest](https://pytest.org/) - Test framework'ü
