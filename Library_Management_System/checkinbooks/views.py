from django.shortcuts import render
from django.db import connection
from .models import Book,Borrower,Fines,BookLoans,Authors,BookAuthors

cursor = connection.cursor()

def index(request):
	books = ""
	message = ""
	get = True
	if(request.method == "POST"):
		if('checkin' in request.POST):
			get = False
			keywords = request.POST['checkin'].split(',')
			comparision = ""
			for keyword in keywords:
				keyword = keyword.strip()
				keyword = "%" + keyword + "%"
				if(comparision != ""):
					comparision += " AND "
				comparision += "(BkAthr.Isbn LIKE '"+keyword+"' OR BkAthr.Title LIKE '"+keyword+"' OR BkAthr.authors LIKE '"+keyword+"' OR BkAthr.Card_id LIKE '"+keyword+"' OR BkAthr.Bname LIKE '"+keyword+"' OR BkAthr.Ssn LIKE '"+keyword+"')"

			query = "SELECT BkAthr.Isbn, BkAthr.Title, BkAthr.authors, BkAthr.Card_id, BkAthr.Bname, BkAthr.Ssn, BkAthr.Loan_id FROM (SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors, Borrower.Card_id, Borrower.Bname, Borrower.Ssn, Book_Loans.Loan_id FROM Book,Book_Authors,Authors,Borrower,Book_Loans WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id AND Book.Isbn = Book_Loans.Isbn AND Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Date_in IS NULL GROUP BY Book.Isbn) AS BkAthr WHERE "+comparision
			cursor.execute(query)
			books = cursor.fetchall()
			return render(request,'checkinbooks/index.html',{'books':books,'message':message,'get':get})
		elif('loanid' in request.POST):
			get = False
			loan_id = request.POST['loanid']
			isbn = request.POST['isbnrtbk'] 
			query = "UPDATE Book_Loans SET Date_in = CURDATE() WHERE Loan_id = '"+ loan_id +"'"
			cursor.execute(query)

			query = "SELECT DATEDIFF(Date_in,Due_date) FROM Book_Loans WHERE Book_Loans.Loan_id = '"+loan_id+"'"
			cursor.execute(query)
			days = cursor.fetchone()[0]

			if(days > 0):
				fine_amt = days*0.25;
				message = "Your fine of amount "+str(fine_amt)+" is due "
				query = "SELECT Paid FROM Fines WHERE Loan_id = '"+ loan_id +"' GROUP BY Loan_id"
				cursor.execute(query)
				fineExist = cursor.fetchone()
				print(fineExist)
				if(fineExist == None):
					query = "INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('"+ loan_id +"','"+ str(fine_amt) +"','0')"
					cursor.execute(query)
				else:
					if(fineExist[0] == 0):
						query = "UPDATE Fines SET Fine_amt = '"+ str(fine_amt) +"' WHERE Loan_id = '"+loan_id+"'"
						cursor.execute(query)

			query = "UPDATE Book SET Availability = '1' WHERE Isbn = '"+isbn+"'"
			cursor.execute(query)
			message += "successfully checked in book."
			return render(request,'checkinbooks/index.html',{'Books':books,'message':message, 'get':get})
		else:
			message = "Please try again."
			return render(request,'checkinbooks/index.html',{'Books':books,'message':message, 'get':get})	
	else:
		return render(request,'checkinbooks/index.html',{'Books':books,'message':message, 'get':get})