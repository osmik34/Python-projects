import os.path
import time
import json


class Book:
    def __init__(self, name, author, release_time, isbn):
        self.name = name
        self.author = author
        self.release_time = release_time
        self.isbn = isbn
        self.available = True
        self.due_time= None

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []
        self.penalty_balance = 0

BOOKS_FILENAME = "books.json"
USER_FILENAME = "users.json"
class Library:
    def __init__(self):
        if os.path.exists(BOOKS_FILENAME):
            with open(BOOKS_FILENAME, "r", encoding="utf-8") as f:
                self.books = json.load(f)
        else:
            with open(BOOKS_FILENAME, "w") as f:
                json.dump([], f, indent=4)
                self.books = {}

        if os.path.exists(USER_FILENAME):
            with open(USER_FILENAME, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        else:
            with open(USER_FILENAME,"w") as f:
                json.dump([],f,indent=4)
                self.users = {}



    def add_book(self, book_dict):
        isbn = str(book_dict["book_isbn"]).strip()
        self.books[isbn] = book_dict



        with open(BOOKS_FILENAME,"w") as f:
            json.dump(self.books,f,indent=4)

        print(f"Kitabxanaya {book_dict["book_name"]} kitabi elave edildi")

    def register_user(self, user_dict):
        userr_id = str(user_dict["user_id"]).strip()
        self.users[userr_id] = user_dict

        self.users[user_dict["userr_id"]] = user_dict
        with open(USER_FILENAME,"w") as f:
            json.dump(self.users,f,indent=4)
        print(f"{user_dict["user_name"]} adli istifadeci elave edildi")

    def borrow_book(self, user_id, isbn):
        us_id = str(user_id).strip()
        isbnn = str(isbn).strip()
        if us_id in self.users and isbnn in self.books:
            user = self.users[us_id]
            book = self.books[isbnn]
            if book.get("available"):
                user["borrowed_books"].append(book["book_name"])
                book["available"] = False
                book["due_time"] = time.time() + 70
                self.save_all()
                print(f"{book.name} kitabi ugurla goturuldu")
            else:
                print("Bu kitab artiq goturulub")
        else:
            print("Istifadeci ve kitab tapilmadi")

    def return_book(self, user_id, isbn):
        user_id = str(user_id).strip()
        isbn = str(isbn).strip()
        user = self.users[user_id]
        book = self.books[isbn]

        user.borrowed_books.remove(book)
        book.available = True
        book.due_time = 0
        delay_time = int(input("Nece gun gecikib? "))
        #geciken her gune 1 azn
        user["penalty_balance"] += delay_time
        print(f"Kitab qaytarildi , Cerime {user["penalty_balance"]} Azn")


my_library = Library()

while True:
    print('''
                    1.Kitab elave et
                    2.Istifadeci elave et
                    3.Kitab gotur
                    4.Kitab qaytar
                    5.Cixis
    ''')

    choose = int(input("Birini sec (1,2,3,4,5) : "))
    if choose == 1:
        book_name = input("Kitabin adi: ")
        book_author = input("Kitabin muellifi: ")
        book_release_time = input("Kitabin ili: ")
        book_isbn = input("Kitabin isbn - i : : ")

        new_book = {
            "book_name" : book_name,
            "book_author" : book_author,
            "book_release_time" : book_release_time,
            "book_isbn" : book_isbn
        }

        my_library.add_book(new_book)

    if choose == 2:
        user_name = input("Istifadeci adi: ")
        user_user_id = input("Istifadeci id - si: ")

        new_user = {
            "user_name" : user_name,
            "user_id" : user_user_id,

        }
        my_library.register_user(new_user)

    if choose == 3:
        user_user_id = input("Istifadeci id - si: ")
        user_isbn = input("Kitabin isbn - i: ")


        my_library.borrow_book(user_user_id,user_isbn )
    if choose == 4:
        user_user_id = input("Istifadeci id - si: ")
        user_isbn = input("Kitabin isbn - i: ")

        my_library.return_book(user_user_id,user_isbn )

    if choose == 5:
        print("Proqramdan cixildi.")
        break
