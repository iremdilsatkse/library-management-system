from library.library import Library

def main():
    library = Library()

    while True:
        print("\n--- Kütüphane Yönetim Sistemi ---")
        print("1. ISBN ile Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Lütfen bir seçenek girin (1-5): ")

        if choice == '1':
            isbn = input("Eklenecek kitabın ISBN numarasını girin: ")
            success, message = library.add_book_by_isbn(isbn)
            print(message)

        elif choice == '2':
            isbn = input("Silinecek kitabın ISBN'sini girin: ")
            success, message = library.remove_book(isbn)
            print(message)

        elif choice == '3':
            print(library.list_books())

        elif choice == '4':
            isbn = input("Aranacak kitabın ISBN'sini girin: ")
            book = library.find_book(isbn)
            if book:
                print(f"Kitap bulundu: {book}")
            else:
                print("Kitap bulunamadı.")
        
        elif choice == '5':
            print("Kütüphane uygulamasından çıkılıyor. Güle güle!")
            break

        else:
            print("Geçersiz seçenek. Lütfen 1 ile 5 arasında bir sayı girin.")

if __name__ == "__main__":
    main()