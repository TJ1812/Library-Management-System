import pymysql

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'library'

myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database)

def createTableBook(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE BOOK(Isbn VARCHAR(10) NOT NULL, Title VARCHAR(255), Availability INT NOT NULL DEFAULT 1, CONSTRAINT BKPK PRIMARY KEY(Isbn));'
    cur.execute(query)
    print("Created Table Book")


def createTableBookAuthors(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE BOOK_AUTHORS(Author_id INT NOT NULL AUTO_INCREMENT, Isbn VARCHAR(10), CONSTRAINT BKAPK PRIMARY KEY(Author_id), CONSTRAINT BKAFK FOREIGN KEY(Isbn) REFERENCES BOOK(Isbn) ON DELETE SET NULL);'
    cur.execute(query)
    print("Created Table Book_Authors")


def createTableAuthors(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE AUTHORS(Author_id INT NOT NULL AUTO_INCREMENT, Name VARCHAR(255) NOT NULL, CONSTRAINT ATHPK PRIMARY KEY(Author_id), CONSTRAINT ATHFK FOREIGN KEY(Author_id) REFERENCES BOOK_AUTHORS(Author_id) ON DELETE CASCADE);'
    cur.execute(query)
    print("Created Table Authors")


def createTableBorrower(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE BORROWER(Card_id INT NOT NULL AUTO_INCREMENT, Ssn VARCHAR(9) NOT NULL UNIQUE, Bname VARCHAR(255), Address VARCHAR(255), Phone VARCHAR(13), CONSTRAINT BRPK PRIMARY KEY(Card_id));'
    cur.execute(query)
    print("Created Table Borrower")

def createTableBookLoans(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE BOOK_LOANS(Loan_id INT NOT NULL AUTO_INCREMENT, Isbn VARCHAR(10),Card_id INT, Date_out DATE, Due_date DATE, Date_in DATE, CONSTRAINT BKLPK PRIMARY KEY(Loan_id), CONSTRAINT BKLFK FOREIGN KEY(Isbn) REFERENCES BOOK(Isbn) ON DELETE SET NULL, CONSTRAINT BKLFKB FOREIGN KEY(Card_id) REFERENCES BORROWER(Card_id) ON DELETE SET NULL);'
    cur.execute(query)
    print("Created Table Book Loans")

def createTableFines(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE FINES(Loan_id INT NOT NULL , Fine_amt REAL NOT NULL DEFAULT 0, CONSTRAINT FNPK PRIMARY KEY(Loan_id), CONSTRAINT FOREIGN KEY(Loan_id) REFERENCES BOOK_LOANS(Loan_id) ON DELETE CASCADE);'
    cur.execute(query)
    print("Created Table Fines")


createTableBook(myConnection)
createTableBookAuthors(myConnection)
createTableAuthors(myConnection)
createTableBorrower(myConnection)
createTableBookLoans(myConnection)
createTableFines(myConnection)
myConnection.close()