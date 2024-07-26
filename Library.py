import hashlib
from datetime import datetime, timedelta

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.role = role

class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.logged_in_user = None
        self.library = Library(
            {
                "vistas": "path/to/vistas.pdf",
                "invention": "path/to/invention.pdf",
                "rich&poor": "path/to/rich&poor.pdf",
                "indian": "path/to/indian.pdf",
                "macroeconomics": "path/to/macroeconomics.pdf",
                "microeconomics": "path/to/microeconomics.pdf"
            }
        )

    def register(self, username, password, role):
        if username in self.users:
            print("Username already exists!")
        else:
            self.users[username] = User(username, password, role)
            print("Registration successful!")

    def login(self, username, password):
        if username in self.users:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if self.users[username].password == hashed_password:
                self.logged_in_user = self.users[username]
                print(f"Login successful! Welcome, {username}.")
            else:
                print("Incorrect password!")
        else:
            print("Username not found!")

    def logout(self):
        self.logged_in_user = None
        print("Logged out successfully!")

class Library:
    def __init__(self, books_with_pdfs):
        self.books = books_with_pdfs
        self.borrowed_books = {}

    def displayAvailableBooks(self):
        print(f"\n{len(self.books)} AVAILABLE BOOKS ARE: ")
        for book in self.books:
            print(" ♦-- " + book)
        print("\n")

    def borrowBook(self, name, bookname):
        if bookname not in self.books:
            print(f"{bookname} BOOK IS NOT AVAILABLE EITHER TAKEN BY SOMEONE ELSE, WAIT UNTIL HE RETURNED.\n")
        else:
            due_date = datetime.now() + timedelta(days=14)
            self.borrowed_books[bookname] = {'borrower': name, 'due_date': due_date}
            print(f"BOOK ISSUED: {bookname}. Please return by {due_date.strftime('%Y-%m-%d')}.\n")
            pdf_path = self.books[bookname]
            print(f"Here is the link to download your book: {pdf_path}")
            del self.books[bookname]

    def returnBook(self, bookname):
        if bookname in self.borrowed_books:
            print("BOOK RETURNED : THANK YOU! \n")
            self.books[bookname] = "path/to/pdf"  # Restore the PDF path (in a real scenario, this should be tracked)
            del self.borrowed_books[bookname]
        else:
            print("This book was not borrowed from this library.\n")

    def donateBook(self, bookname, pdf_path):
        print("BOOK DONATED : THANK YOU VERY MUCH, HAVE A GREAT DAY AHEAD.\n")
        self.books[bookname] = pdf_path

    def check_overdue_books(self):
        today = datetime.now()
        for book, info in self.borrowed_books.items():
            if info['due_date'] < today:
                print(f"Book {book} is overdue. Borrower: {info['borrower']}")

class Student:
    def requestBook(self):
        print("So, you want to borrow a book!")
        self.book = input("Enter name of the book you want to borrow: ")
        return self.book

    def returnBook(self):
        print("So, you want to return a book!")
        self.book = input("Enter name of the book you want to return: ")
        return self.book

    def donateBook(self):
        print("Okay! You want to donate a book!")
        self.book = input("Enter name of the book you want to donate: ")
        self.pdf_path = input("Enter path to the PDF file: ")
        return self.book, self.pdf_path

if __name__ == "__main__":
    system = LibrarySystem()
    student = Student()

    print("\t\t\t\t\t\t\t♦♦♦♦♦♦♦ WELCOME TO THE LIBRARY ♦♦♦♦♦♦♦\n")
    print("""REGISTER OR LOGIN TO USE THE LIBRARY:
1. Register
2. Login
3. Exit
""")

    while True:
        try:
            usr_response = int(input("Enter your choice: "))
            if usr_response == 1:  # register
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role (student/librarian): ")
                system.register(username, password, role)
            elif usr_response == 2:  # login
                username = input("Enter username: ")
                password = input("Enter password: ")
                system.login(username, password)
                if system.logged_in_user:
                    while True:
                        print("""\nCHOOSE WHAT YOU WANT TO DO:
1. List all books
2. Borrow books
3. Return books
4. Donate books
5. Track books
6. Check overdue books
7. Logout
""")
                        user_choice = int(input("Enter your choice: "))
                        if user_choice == 1:  # listing
                            system.library.displayAvailableBooks()
                        elif user_choice == 2:  # borrow
                            if system.logged_in_user.role == "student":
                                system.library.borrowBook(system.logged_in_user.username, student.requestBook())
                            else:
                                print("Only students can borrow books.")
                        elif user_choice == 3:  # return
                            if system.logged_in_user.role == "student":
                                system.library.returnBook(student.returnBook())
                            else:
                                print("Only students can return books.")
                        elif user_choice == 4:  # donate
                            bookname, pdf_path = student.donateBook()
                            system.library.donateBook(bookname, pdf_path)
                        elif user_choice == 5:  # track
                            for book, info in system.library.borrowed_books.items():
                                print(f"{book} book is taken/issued by {info['borrower']}. Due on {info['due_date'].strftime('%Y-%m-%d')}.")
                            if len(system.library.borrowed_books) == 0:
                                print("NO BOOKS ARE ISSUED! \n")
                        elif user_choice == 6:  # check overdue books
                            system.library.check_overdue_books()
                        elif user_choice == 7:  # logout
                            system.logout()
                            break
                        else:
                            print("INVALID INPUT! \n")
            elif usr_response == 3:  # exit
                print("THANK YOU! \n")
                exit()
            else:
                print("INVALID INPUT! \n")
        except Exception as e:  # catch errors
            print(f"{e} ---> INVALID INPUT! \n")


    
