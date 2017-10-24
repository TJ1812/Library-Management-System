from django.shortcuts import render
from .models import Borrower,BookLoans,Fines
from django.db import connection

cursor = connection.cursor()

def index(request):
	fines = ""
	message = ""
	get = True
	if(request.method == 'POST'):
		if('searchfines' in request.POST):
			get = False
			keywords = request.POST['searchfines'].split(',')
			comparision = ""
			for keyword in keywords:
				keyword = keyword.strip()
				keyword = "%" + keyword + "%"
				if(comparision != ""):
					comparision += " AND "
				comparision += "(BrrFine.Card_id LIKE '"+keyword+"' OR BrrFine.Ssn LIKE '"+keyword+"' OR BrrFine.Bname LIKE '"+keyword+"')"

			query = "SELECT BrrFine.Card_id, BrrFine.Ssn, BrrFine.Bname, BrrFine.Totalfine, BrrFine.Loan_id FROM (SELECT Borrower.Card_id, Borrower.Ssn, Borrower.Bname, SUM(Fines.Fine_amt) Totalfine, Book_Loans.Loan_id FROM Borrower,Book_Loans,Fines WHERE Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Loan_id = Fines.Loan_id AND Fines.Paid = '0' AND Book_Loans.Date_in IS NOT NULL GROUP BY Borrower.Card_id) AS BrrFine WHERE "+comparision
			cursor.execute(query)
			print(query)
			fines = cursor.fetchall()
			return render(request,'payfine/index.html',{'fines':fines,'message':message,'get':get})

		elif('refreshfines' in request.POST):
			query = "SELECT Loan_id, DATEDIFF(CURDATE(),Due_date)*0.25 difference FROM Book_Loans WHERE DATEDIFF(CURDATE(),Due_date)*0.25 > '0'"
			cursor.execute(query)
			results = cursor.fetchall()
			for result in results:
				query = "SELECT Loan_id FROM Fines WHERE Loan_id = '"+str(result[0])+"'"
				cursor.execute(query)
				if(cursor.fetchone() == None):
					query = "INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('"+ str(result[0]) +"', '"+str(result[1])+"', '0')"
					cursor.execute(query)
				else:
					query = "UPDATE Fines SET Fines.Fine_amt = '"+str(result[1])+"' WHERE Fines.Loan_id = '"+str(result[0])+"' AND Fines.Paid = '0'"
					cursor.execute(query)

			message = "Successfully Refreshed Fines"
			return render(request,'payfine/index.html',{'fines':fines,'message':message,'get':get})

		elif('cardnumber' in request.POST):
			cardnumber = request.POST['cardnumber']
			query = "SELECT Loan_id FROM Book_Loans WHERE Date_in IS NOT NULL AND Card_id = '"+str(cardnumber)+"'"
			cursor.execute(query)
			loanids = cursor.fetchall();
			for loanid in loanids:
				query = "UPDATE Fines SET Fines.Paid = '1' WHERE Fines.Loan_id = '"+str(loanid[0])+"' AND Fines.Paid = '0'"
				cursor.execute(query)
			message = "Payment Successful."
			return render(request,'payfine/index.html',{'fines':fines,'message':message,'get':get})

		else:
			message = "Something went wrong please try again."
			return render(request,'payfine/index.html',{'fines':fines,'message':message,'get':get})
	else:
		return render(request,'payfine/index.html',{'fines':fines,'message':message,'get':get})