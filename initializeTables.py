import pandas as pd
import pymysql

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'library'

myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database)
cur = myConnection.cursor()
cur.execute("DELETE FROM Book;")
cur.execute("DELETE FROM Book_Authors;")
cur.execute("DELETE FROM Authors;")
cur.execute("ALTER TABLE Book_Authors AUTO_INCREMENT = 1;")
cur.execute("ALTER TABLE Authors AUTO_INCREMENT = 1;")
cur.execute("ALTER TABLE Borrower AUTO_INCREMENT = 1;")
cur.execute("ALTER TABLE Book_Loans AUTO_INCREMENT = 1;")
cur.execute("ALTER TABLE Fines AUTO_INCREMENT = 1;")

books = pd.read_csv('books.csv')
borrowers = pd.read_csv('borrowers.csv')

def insertIntoBook(conn, data, key):
	isbn10 = data.get_value(key,'ISBN10')
	title = data.get_value(key,'Title')
	authors = str(data.get_value(key,'Author')).split(',')
	availabitity = 1
	cur = conn.cursor()
	query = 'INSERT INTO Book VALUES("'+ str(isbn10) +'","'+ str(title) +'","'+ str(availabitity) +'");'
	cur.execute(query)

	for author in authors:
		query1 = 'INSERT INTO Book_Authors(Isbn) VALUES("'+ str(isbn10) +'");'
		cur.execute(query1)
	
	for author in authors:
		query2 = 'INSERT INTO Authors(Name) VALUES("'+ author +'");'
		cur.execute(query2)

def insertIntoBorrower(conn, data, key):
	ssn = str(data.get_value(key,'id'))
	bname = str(data.get_value(key,'first_name')) +" "+ str(data.get_value(key,'last_name'))
	address = str(data.get_value(key,'address')) +","+ str(data.get_value(key,'city')) +","+ str(data.get_value(key,'state'))
	phone = str(data.get_value(key,'phone'))

	query = 'INSERT INTO Borrower(Ssn,Bname,Address,Phone) VALUES("'+ ssn +'","'+ bname +'","'+ address +'","'+ phone +'");'
	cur.execute(query)

for i in range(1,len(books)+1):
	insertIntoBook(myConnection,books[i-1:i],i-1)

for i in range(1,len(borrowers)+1):
	insertIntoBorrower(myConnection,borrowers[i-1:i],i-1)

print("Successfully initialized all tables")

myConnection.commit()
myConnection.close()